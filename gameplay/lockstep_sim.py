"""确定性锁步模拟的公共契约。

这里的函数用于把"按本地时间/本地帧号/对象身份"驱动的逻辑，改成
"按整数 tick/显式帧号/稳定排序键"驱动的逻辑，从而保证十人联机时
各端在相同输入下得到逐位一致的结果。
"""

from fractions import Fraction


def _exact(value):
    """把 int/float/Decimal/Fraction 转成精确有理数，避免二进制浮点误差。"""
    if isinstance(value, Fraction):
        return value
    return Fraction(str(value))


def tick_from_time(time, rate):
    """整数 tick。

    tick 只由整数累加得到：用精确有理数把 ``time * rate`` 向下取整，
    避免浮点累加在长时间运行后偏出半帧。负时间按 0 处理。
    """
    if rate <= 0:
        raise ValueError("rate must be positive")
    ticks = _exact(time) * _exact(rate)
    if ticks <= 0:
        return 0
    return ticks.numerator // ticks.denominator


def input_slot(tick, delay):
    """输入帧号。

    输入槽位按目标 tick 与固定输入延迟计算，与客户端本地帧率无关，
    因此不同帧率的客户端会把同一份输入放进同一个 tick。
    """
    if delay < 0:
        raise ValueError("delay must be non-negative")
    return max(0, tick - delay)


def checksum(fields):
    """全量校验。

    校验和必须覆盖该 tick 的全部可观测状态（位置、物理接触点、
    随机数状态等），调用方负责把所有字段传进来；这里对它们求和。
    """
    return sum(fields)


def seed_from(seed, tick):
    """统一种子。

    每个 tick 的随机种子只由"初始种子 + tick"决定，所有端用同一个
    初始种子即可得到同一序列，不再依赖主机时间。
    """
    if tick < 0:
        raise ValueError("tick must be non-negative")
    return (seed + tick) & 0xFFFFFFFFFFFFFFFF


def fixed_step(dt):
    """定点步长。

    把秒转换为整数时间单位（毫秒），物理计算只使用整数，避免不同
    平台浮点结果不一致。
    """
    if dt < 0:
        raise ValueError("dt must be non-negative")
    return round(float(dt) * 1000)


def entity_order(ids):
    """实体顺序。

    实体遍历顺序由稳定、可复现的整数 id 排序决定，而不是哈希表
    插入/删除后的内部顺序。
    """
    return sorted(ids)


def packet_fill(missing, last):
    """丢包补齐。

    某个输入槽丢包时，所有客户端都确定性地复用上一份已确认输入；
    返回 ``last``。未丢包时返回 ``None``，表示使用刚收到的输入。
    """
    if missing:
        return last
    return None


def reconnect_replay(from_tick, to_tick):
    """重连回放。

    重连时从缺失的第一个 tick 开始，逐个回放输入直到（不含）当前
    tick，而不是只发一份世界快照把角色直接塞进墙里。
    """
    if from_tick < 0 or to_tick < 0:
        raise ValueError("ticks must be non-negative")
    if from_tick >= to_tick:
        return []
    return list(range(from_tick, to_tick))


def buffer_limit(size, max_size):
    """缓冲上限。

    锁步缓冲不得超过固定上限，慢客户端不会让缓冲无限增长，快客户端
    也不必无限等待。
    """
    if max_size < 0:
        raise ValueError("max_size must be non-negative")
    return max(0, min(size, max_size))


def dilation(local_rate, base_rate):
    """统一膨胀。

    时间膨胀系数只由本地帧率与基准帧率之比决定（基准/本地），慢设备
    通过膨胀追帧而不是把游戏整体变慢。
    """
    if local_rate <= 0 or base_rate <= 0:
        raise ValueError("rates must be positive")
    return base_rate / local_rate


def replay_key(tick, entity):
    """回放校验。

    回放记录以 (tick, entity) 作为稳定键，配合全量校验和即可定位
    第一次分叉的位置。
    """
    return f"{tick}:{entity}"


def stable_sort(keys):
    """稳定排序。

    使用显式、可复现的排序键；相等键保持原始相对顺序，不依赖对象
    地址。传入 (key, payload) 时只比较 key。
    """
    return sorted(
        keys,
        key=lambda item: item[0] if isinstance(item, tuple) else item,
    )


def physics_steps(frame_time, step):
    """统一步长。

    每帧物理迭代次数由统一的整数步长整除得到，服务器和客户端使用
    同一步长与同一计数规则，爆炸冲击波范围因此一致。
    """
    step_units = fixed_step(step)
    if step_units <= 0:
        raise ValueError("step must be positive")
    return fixed_step(frame_time) // step_units


def divergence(local, remote):
    """分叉判定。

    两端同一 tick 的状态（或校验和）不同即判定发生分叉。
    """
    return local != remote


def history_window(tick, size):
    """历史窗口。

    历史记录使用固定大小的环形窗口，槽位由 tick 对窗口大小取模
    得到，因此内存有界且各端一致。
    """
    if size <= 0:
        raise ValueError("size must be positive")
    return tick % size
