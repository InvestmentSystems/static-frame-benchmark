
import static_frame as sf
from static_frame.core.interface import InterfaceGroup

from types import SimpleNamespace
import frame_fixtures as ff
from .prototype import apply_prototype

from .fixtures_reference import FRAME_G
from .fixtures_reference import FRAME_H

class Prototype:

    def asv_time_setitem(self, ns: SimpleNamespace):
        f = sf.FrameGO(index=ns.frame.index)
        for s in ns.frame_series:
            f[s.name] = s

    def asv_time_extend(self, ns: SimpleNamespace):
        f = sf.FrameGO(index=ns.frame.index)
        f.extend(ns.frame_part1)
        f.extend(ns.frame_part2)


def create_fixtures(fixture: str):
    frame = ff.parse(fixture)
    mid_iloc = len(frame.columns) // 2
    frame_part1 = frame.iloc[:, :mid_iloc].to_frame_go()
    frame_part2 = frame.iloc[:, mid_iloc:]

    # mutate index so as to force reindex, only add 10 series as this test can be slow
    frame_series = [frame.loc[sf.ILoc[1:], col] for col in frame.columns[:10]]

    return SimpleNamespace(
            frame=frame,
            frame_part1=frame_part1,
            frame_part2=frame_part2,
            frame_series=frame_series,
            )

@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Method)
class FrameG:

    FIXTURE = FRAME_G

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE)


@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Method)
class FrameH:

    FIXTURE = FRAME_H

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE)
