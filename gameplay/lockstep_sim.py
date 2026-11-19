"""第 63 批：十人联机打到第三关开始漂移，回放里同一颗手雷炸在不同位置，掉线重..."""

def tick_from_time(time, rate):
    """整数 tick。"""
    raise NotImplementedError("TODO: tick_from_time")

def input_slot(tick, delay):
    """输入帧号。"""
    raise NotImplementedError("TODO: input_slot")

def checksum(fields):
    """全量校验。"""
    raise NotImplementedError("TODO: checksum")

def seed_from(seed, tick):
    """统一种子。"""
    raise NotImplementedError("TODO: seed_from")

def fixed_step(dt):
    """定点步长。"""
    raise NotImplementedError("TODO: fixed_step")

def entity_order(ids):
    """实体顺序。"""
    raise NotImplementedError("TODO: entity_order")

def packet_fill(missing, last):
    """丢包补齐。"""
    raise NotImplementedError("TODO: packet_fill")

def reconnect_replay(from_tick, to_tick):
    """重连回放。"""
    raise NotImplementedError("TODO: reconnect_replay")

def buffer_limit(size, max_size):
    """缓冲上限。"""
    raise NotImplementedError("TODO: buffer_limit")

def dilation(local_rate, base_rate):
    """统一膨胀。"""
    raise NotImplementedError("TODO: dilation")

def replay_key(tick, entity):
    """回放校验。"""
    raise NotImplementedError("TODO: replay_key")

def stable_sort(keys):
    """稳定排序。"""
    raise NotImplementedError("TODO: stable_sort")

def physics_steps(frame_time, step):
    """统一步长。"""
    raise NotImplementedError("TODO: physics_steps")

def divergence(local, remote):
    """分叉判定。"""
    raise NotImplementedError("TODO: divergence")

def history_window(tick, size):
    """历史窗口。"""
    raise NotImplementedError("TODO: history_window")
