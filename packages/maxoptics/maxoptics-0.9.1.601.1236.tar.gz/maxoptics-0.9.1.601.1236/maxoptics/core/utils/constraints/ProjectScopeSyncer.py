from collections import defaultdict

from maxoptics.core.logger import info_print
from maxoptics.var.config import Config
from maxoptics.var.constraints import project_scope


class Restrainer:
    def __init__(self):
        self.all_hkts = project_scope()
        self.trigger_map = defaultdict(list)
        for signals, filter_, functor in self.all_hkts:
            for signal in signals:
                if (filter_, functor) not in self.trigger_map[signal]:
                    self.trigger_map[signal].append((filter_, functor))

        self.trigger_map = dict(self.trigger_map)

    def emit(self, project, signal, actor, escape=[]):
        if Config.DisableConstraints:
            matched_hkts = []
        else:
            matched_hkts = self.trigger_map.get(signal, [])
        for filter_, functor in matched_hkts:
            if "*" in escape or signal in escape:
                ...
            else:
                if not filter_(project, actor):
                    continue

                if Config.Verbose:
                    if hasattr(actor, "name"):
                        actor_repr = actor.name
                    elif isinstance(actor, (int, str, float)):
                        actor_repr = actor
                    else:
                        actor_repr = actor.__class__.__name__

                    if actor:
                        msg = f"(PC) {signal} on {actor_repr}:"
                    else:
                        msg = f"(PC) {signal}:"

                    with info_print(msg):
                        functor(project, actor)
                else:
                    functor(project, actor)
