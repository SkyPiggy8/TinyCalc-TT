# TinyCalc-TT · 参考形象 VGA 显示芯片

项目已从计算器改为显示参考图中的圆头、绿色眼睛、大肚子、双手抱肚的黄色角色。
仓库名 `TinyCalc-TT` 保留不变。现在的电路是专用图形显示器，没有 CPU 指令集。

![实际综合逻辑门仿真输出](preview/frame_00.png)

显示素材按用户提供的参考图重新制作；不是上一版正面、小身体、张嘴的简化图案。
`assets/character_source.png` 为按参考形象生成的项目素材，`preview/sprite.png`
为**真正写入硬件 ROM 的像素与色彩**；不是把高分辨率效果图当作芯片画面。

## 已实现

- 48×96 像素图案，4 位索引、16 项调色板，固定数据共 18,432 bits。
- 内部常量 ROM 生成像素，不需要 ESP32、外部图片存储器或电脑实时传图。
- 640×480 VGA，25.175 MHz 像素时钟，约 59.94 Hz，TinyVGA 标准引脚。
- 4 倍整数放大，角色显示尺寸 192×384，默认位置 (224,48)，白色背景。
- 默认上下轻微摆动；`ui_in[0]=1` 暂停动画。保留参考图的闭嘴表情，无眨眼变形。

## 可复核的验证

`reports/video_verification.txt` 记录综合后通用逻辑门仿真结果：

1. 连续 840,000 个像素时钟，检查两帧的计数、同步和 RGB 输出。
2. 在指定相位 0、16、60 分别运行一整帧，对比独立的 `assets/sprite.json`
   图案模型，逐像素检查 ROM 解码、调色板、坐标和缩放。
3. 检查动画冻结、输出禁用和复位。

相位 16/60 直接初始化寄存器进入，不声称连续等待运行了 60 帧。
`preview/animation.gif` 是选定状态的示意串联，播放时长不是硬件真实周期。

## 面积和版图状态

当前配置为 **SKY130，1×2 tiles**。直接映射使用 1,236 个标准单元，
单元面积约 12,931.152 μm²；单个 tile 的占用约 72%，因此给正式布线留出余量。
这不是经过工艺库时序优化后的最优面积，也不证明 1×1 一定放不下。

`layout/nailong_placement_ONLY.gds` 包含当前电路的真实 SKY130 单元几何，
但只是初始行布局，坐标由脚本生成，不是已经逐单元手工优化的完整版图。
完整信号布线、供电、时钟、DRC、LVS 和寄生时序尚未完成。
官方工作流产生的自动硬化版图与这个布局检查点是两个不同实现，不能互相代替验证。

## 外接硬件

Tiny Tapeout 开发板、TinyVGA 电阻 DAC 模块、VGA 线和支持该模式的显示器。
HDMI-only 显示器需要**有源 VGA 输入 → HDMI 输出**转换器。
不能用被动转接线，也不能把芯片数字 RGB 引脚直接连到 VGA 模拟输入。
完整引脚、时序和操作说明见 [docs/info.md](docs/info.md)。

## 复现

```sh
pip install -r requirements-tools.txt
python scripts/encode_sprite.py
mkdir -p build
yowasp-yosys -s scripts/synth.ys > build/synth.log
python scripts/gate_video_test.py
python scripts/preview.py
python scripts/placement_checkpoint.py --cells third_party/sky130_fd_sc_hd
```

综合也可使用原生 `yosys` 或 `python scripts/run_yosys.py`；门级仿真器需要 g++。
传统 RTL 测试用 Icarus Verilog：`pip install -r test/requirements.txt && cd test && make`。
引脚保持 Tiny Tapeout 标准包装，顶层为 `tt_um_skypiggy8_nailong`。
根目录保留 `info.yaml / src / test / docs / .github/workflows` 官方模板结构。

源素材提示词和编码规则见 [assets/PROMPT.md](assets/PROMPT.md)。
本地功能验证通过不等于可制造；以在线 GDS、precheck、门级和时序检查结果为准。
