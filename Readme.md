# RoboCasa365 · GPT6Astra Direct 轨迹与成功率归档

本仓库汇总两批可独立核查的 RoboCasa365 GPT Direct 完整原生轨迹，模型为 `gpt-6-astra`。两批在不同机器、不同时间产出，统计口径各自独立，**不能把两批数字相加或互相修正**。

## 0. 批次与目录对照

### 0.1 两个批次

| 批次 | 生成时间（北京时间） | 覆盖子集 / scene | 规模 | 仓库内目录 | Release |
|---|---|---|---|---|---|
| `202611031026` | 2026-11-03 10:59 | Composite-Unseen/pretrain、Composite-Seen/target、Composite-Unseen/target | 245,761 文件，原始 74.530 GB，压缩 46.051 GB，26 卷 | `catalog/` `manifests/` `reports/` `tools/` | `direct-archive-20261103` |
| `202611031607` | 2026-11-03 16:07 | Atomic-Seen/pretrain、Composite-Seen/pretrain、Composite-Seen/target | 174 回合，46,098 个轨迹文件，22,044 张 RGB，11 个分包（4,119,784,130 字节） | `docs/` `metadata/` `scripts/` `statistics/` | `direct-trajectories-20261103` |

两批各自的成功率：

| 子集 | scene | 批次 `202611031026` | 批次 `202611031607` |
|---|---|---|---|
| Atomic-Seen | pretrain | 无本机轨迹（只有异机导入成绩参考） | 38/65 = 58.46% |
| Composite-Seen | pretrain | 无本机轨迹（只有异机导入成绩参考） | 16/55 = 29.09% |
| Composite-Seen | target | 10/55 = 18.18% | 10/54 = 18.52%（原合同 10/56 = 17.86%） |
| Composite-Unseen | pretrain | 26/55 = 47.27% | — |
| Composite-Unseen | target | 37/80 = 46.25% | — |

批次 `202611031607` 正好补上了批次 `202611031026` 当时只有导入成绩参考的两组（Atomic-Seen/pretrain、Composite-Seen/pretrain）的完整轨迹，并另外独立提供了一版 Composite-Seen/target。

### 0.2 同一子集的口径差异

Composite-Seen/target 在两批中都出现，但分母不同：批次 `202611031026` 为 **10/55 = 18.18%**（55 条原生完整记录，另 2 条 PolicyStop 提前停止不计入分母），批次 `202611031607` 为 **10/54 = 18.52%**（54 条完整终局，原合同 10/56 = 17.86%）。两批对“完整”的定义和接纳记录数不同，差 1 条记录，本次**不做合并、也不互相覆盖**；引用时请连同批次号一起写明。

---

## 第一部分 完整 run 目录归档（批次 `202611031026`）

### 1. 基线范围与 SR

| RoboCasa365 子集 | scene | 任务数 | 接纳记录 | 原生完整记录 | 成功 | 原生失败 | 提前停止 | micro SR |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Composite-Unseen | pretrain | 11 | 55 | 55 | 26 | 29 | 0 | 47.27% |
| Composite-Seen | target | 16 | 57 | 55 | 10 | 45 | 2 | 18.18% |
| Composite-Unseen | target | 16 | 80 | 80 | 37 | 43 | 0 | 46.25% |

合计 **192 条接纳记录，190 条原生完整记录，73 条成功**。这里“原生完整”指 native success，或未被基础设施标为无效且实际执行达到原生 horizon；流程层 `status=complete` 并不自动表示原生完整。表内 SR = 成功数 / 原生完整记录数。

Composite-Seen/target 原计划 58 条，当前接纳 57 条；其中 2 条 policy/其他提前停止不计入本表原生失败分母，另有 1 条缺失／基础设施问题。因此 18.18% 是 10/55，不能写作完成了全部计划、也不能默默把早停算作原生失败。若按接纳记录把早停计失败，结果为 10/57=17.54%；按计划 58 条的完成情况应另行报告。

Composite-Unseen/pretrain 的 reasoning effort 混有 `high` 与 `xhigh`，逐记录原值保留；另外两组为 `high`。实际模型标识见原始结果及索引，不能把本批概括为统一 effort 的新控制实验。

三个最终接纳面板按原始输出目录去重，不能累加历史续跑目录中继承的 `ACCEPTED_RESULTS.json`。39 个主 run 目录共找到 **277 个 `episode_result.json`**，其中还包含重试、基础设施失败、smoke 与开发记录；它们不等于 277 条独立正式基线。只有状态而没有结果文件的中断尝试仍在原始归档中，277 也不是历史尝试总数的保证。

本批不包含 Atomic-Seen/pretrain 与 Composite-Seen/pretrain 的本机轨迹；这两组的完整轨迹见第二部分（批次 `202611031607`）。

### 2. 数据分卷

分卷文件名均为 `202611031026_GPT6AstraDirect_<组名>.tar.zst.partNNN`，放在 Release `direct-archive-20261103`。

| 组名 | 内容 | 文件数 | 原始字节量 GB | 压缩后 GB | 分卷数 |
|---|---|---:|---:|---:|---:|
| `CompositeUnseen_pretrain` | Unseen/pretrain 主线及早期重试/开发记录 | 69,502 | 18.571 | 11.948 | 6 |
| `CompositeSeen_target` | Seen/target 主线及重试/续跑记录 | 81,041 | 26.775 | 14.393 | 8 |
| `CompositeUnseen_target` | Unseen/target 主线及重试/续跑记录 | 90,543 | 24.266 | 15.258 | 8 |
| `references_and_early_diagnostics` | 历史 K1 Direct、冻结源码、复现工具与来源报告 | 2,945 | 4.684 | 4.224 | 3 |
| `link_closure` | 可找到的原 agent 链接目标，转存为普通文件 | 1,730 | 0.235 | 0.228 | 1 |

总计 **245,761 个文件，原始 74.530 GB，压缩 46.051 GB，26 个分卷**。GB 按 10⁹ 字节；精确长度、每卷名称及 SHA256 均在 `publication_index.json`。

每卷上限 **1,900 MiB = 1,992,294,400 字节**，末卷较小。它们是同一 zstd 压缩流的连续片段，**不能单独解压某一个 part**；应按编号拼接。三个主数据组按历史 run 目录归组，内部可能包含早期开发／失败记录，组名不等于其中每个文件都属于最终基线面板。判断正式结果应核对各组最终 run 的原始 `ACCEPTED_RESULTS.json`，不能累加继承清单。

解包后各组统一合入：

```text
GPT6AstraDirect/
├── runs/<历史run目录>/
│   ├── frozen/、SUMMARY.json、ACCEPTED_RESULTS.json …
│   └── formal|development|smoke/<任务>/<原轨迹目录>/attempt_*/
│       ├── episode_result.json、episode_status.json
│       ├── token_usage.json、token_usage_events.jsonl
│       ├── agent_events.jsonl
│       ├── evaluator/
│       │   ├── native_actions.jsonl、native_checker.jsonl
│       │   ├── initial.xml、initial_state.npz、initial_metadata.json
│       │   └── simulator_result.json、runtime_manifest.json …
│       └── codex/
│           ├── rpc_in.jsonl、rpc_out.jsonl …
│           └── agent/observations/request_*/
│               ├── observation.json
│               ├── robot0_agentview_left.png
│               ├── robot0_agentview_right.png
│               └── robot0_eye_in_hand.png
├── historical_direct_with_perception/  # 早期 K1 工程/诊断，单独保留
├── reproduction_tools/
└── references/ …                       # 以逐文件 manifest 中的路径为准
```

不同历史 run 的布局有差异；全部相对路径以 `manifests/*.files.jsonl.gz` 为准。早期 K1 使用额外感知工具，不能和后期 Direct 基线合并报告 SR。

### 3. 如何找到并回看一次 rollout

先选对应子集／scene 的归档组，解包后在 `GPT6AstraDirect/runs/` 按任务目录查找。主线、开发、smoke、重试按原目录保留；最终接纳记录应使用下面三个最终 run 的原始 `ACCEPTED_RESULTS.json` 核对，其中记录的原始输出路径应改为解包目录下的相应相对位置：

- Composite-Unseen/pretrain：`20261008T0818Z_reboot_serial_resume`。
- Composite-Seen/target：`20261016_seen_target_gpu3_retry42_resume`。
- Composite-Unseen/target：`20261026T181500Z_composite_unseen_target_harnesscl_coexist_resume8`。

查看 `episode_result.json` 的 `native_success`、`control_steps`、`horizon`、reasoning effort 与费用状态。三相机图像通常位于 `codex/agent/observations/request_*`，按请求编号顺序回看，并结合 `observation.json`、动作账本、环境回执及 RPC 判断实际执行过程。保存的是记录时的观测帧，不保证是连续 20 Hz 视频，也不保证每个历史中断都有全部图像。

费用记录保留原始用量与未知标记；`usage_complete=false` 或终局用量未知不能当作零成本。原始 `initial.xml`/状态数组的存在不表示已验证跨机器精确恢复；本次没有重放物理或重新验收任务成功语义。

### 4. 下载、校验与解包

从 Release `direct-archive-20261103` 下载所需数据组的**全部**分卷；建议同时下载 `202611031026_metadata.zip` 和 `202611031026_SHA256SUMS.txt`。仅回看一个子集可只取该数据组；为补齐 agent 记录还应下载 `link_closure`。历史工具和报告位于 `references_and_early_diagnostics`。

在仓库根目录运行（Python 3；`--payload` 另需 `zstd`）：

```bash
# 只检查分卷 SHA256，不解压
python tools/verify_archive.py --directory /path/to/downloads

# 只验一个组，含每个内部文件 SHA256 和 zstd 尾校验
python tools/verify_archive.py --directory /path/to/downloads \
  --group CompositeUnseen_target --payload
```

校验 metadata ZIP 及全部已下载分卷也可在下载目录执行：

```bash
sha256sum -c 202611031026_SHA256SUMS.txt
```

上述 SHA 清单包含整个交付集，少下文件会报告缺失；选择性下载请使用 `--group`。全量下载并解包 metadata ZIP 后，可用 `--payload` 不加 `--group` 完整验真。

解包一个数据组的示例（先完成校验；在存放分卷的目录执行）：

```bash
mkdir -p data
cat 202611031026_GPT6AstraDirect_CompositeUnseen_target.tar.zst.part* \
  | zstd -dc --memory=512MB | tar -xf - -C data
```

其余组依次替换组名，解到同一个 `data/` 即可。顺序固定的三位 part 编号可直接按文件名拼接。完整解包需要约 75 GB 文件内容空间，另预留文件系统开销；若同时保留下载分卷，还需加上压缩文件体积。没有 zstd 时先安装系统 `zstd`，不要把 part 当作 ZIP。

### 5. 完整逐任务结果

以下为这三组最终接纳面板的全部任务；不额外生成逐 seed 表。每任务可能因早停／缺项而样本数不相等，所以全体 micro SR 不能直接称为逐任务平均 SR。

| 子集 | scene | 任务 | 原生完整 | 成功 | 原生失败 | 提前停止 | SR | effort |
|---|---|---|---:|---:|---:|---:|---:|---|
| Composite-Unseen | pretrain | ArrangeBreadBasket | 5 | 2 | 3 | 0 | 40.00% | xhigh |
| Composite-Unseen | pretrain | ArrangeTea | 5 | 4 | 1 | 0 | 80.00% | high;xhigh |
| Composite-Unseen | pretrain | CategorizeCondiments | 5 | 2 | 3 | 0 | 40.00% | high |
| Composite-Unseen | pretrain | CuttingToolSelection | 5 | 2 | 3 | 0 | 40.00% | high |
| Composite-Unseen | pretrain | GarnishPancake | 5 | 2 | 3 | 0 | 40.00% | high |
| Composite-Unseen | pretrain | PanTransfer | 5 | 3 | 2 | 0 | 60.00% | high |
| Composite-Unseen | pretrain | PortionHotDogs | 5 | 4 | 1 | 0 | 80.00% | high |
| Composite-Unseen | pretrain | SeparateFreezerRack | 5 | 0 | 5 | 0 | 0.00% | high |
| Composite-Unseen | pretrain | WaffleReheat | 5 | 3 | 2 | 0 | 60.00% | high |
| Composite-Unseen | pretrain | WashFruitColander | 5 | 4 | 1 | 0 | 80.00% | high |
| Composite-Unseen | pretrain | WeighIngredients | 5 | 0 | 5 | 0 | 0.00% | high |
| Composite-Seen | target | DeliverStraw | 5 | 1 | 4 | 0 | 20.00% | high |
| Composite-Seen | target | GetToastedBread | 3 | 0 | 3 | 0 | 0.00% | high |
| Composite-Seen | target | KettleBoiling | 5 | 4 | 1 | 0 | 80.00% | high |
| Composite-Seen | target | LoadDishwasher | 3 | 0 | 3 | 0 | 0.00% | high |
| Composite-Seen | target | PackIdenticalLunches | 5 | 1 | 4 | 0 | 20.00% | high |
| Composite-Seen | target | PreSoakPan | 3 | 0 | 3 | 0 | 0.00% | high |
| Composite-Seen | target | PrepareCoffee | 3 | 1 | 2 | 0 | 33.33% | high |
| Composite-Seen | target | RinseSinkBasin | 3 | 0 | 3 | 0 | 0.00% | high |
| Composite-Seen | target | ScrubCuttingBoard | 3 | 1 | 2 | 0 | 33.33% | high |
| Composite-Seen | target | SearingMeat | 5 | 2 | 3 | 0 | 40.00% | high |
| Composite-Seen | target | SetUpCuttingStation | 3 | 0 | 3 | 0 | 0.00% | high |
| Composite-Seen | target | StackBowlsCabinet | 3 | 0 | 3 | 0 | 0.00% | high |
| Composite-Seen | target | SteamInMicrowave | 3 | 0 | 3 | 0 | 0.00% | high |
| Composite-Seen | target | StirVegetables | 2 | 0 | 2 | 1 | 0.00% | high |
| Composite-Seen | target | StoreLeftoversInBowl | 1 | 0 | 1 | 1 | 0.00% | high |
| Composite-Seen | target | WashLettuce | 5 | 0 | 5 | 0 | 0.00% | high |
| Composite-Unseen | target | ArrangeBreadBasket | 5 | 2 | 3 | 0 | 40.00% | high |
| Composite-Unseen | target | ArrangeTea | 5 | 2 | 3 | 0 | 40.00% | high |
| Composite-Unseen | target | BreadSelection | 5 | 4 | 1 | 0 | 80.00% | high |
| Composite-Unseen | target | CategorizeCondiments | 5 | 1 | 4 | 0 | 20.00% | high |
| Composite-Unseen | target | CuttingToolSelection | 5 | 4 | 1 | 0 | 80.00% | high |
| Composite-Unseen | target | GarnishPancake | 5 | 3 | 2 | 0 | 60.00% | high |
| Composite-Unseen | target | GatherTableware | 5 | 1 | 4 | 0 | 20.00% | high |
| Composite-Unseen | target | HeatKebabSandwich | 5 | 2 | 3 | 0 | 40.00% | high |
| Composite-Unseen | target | MakeIceLemonade | 5 | 2 | 3 | 0 | 40.00% | high |
| Composite-Unseen | target | PanTransfer | 5 | 4 | 1 | 0 | 80.00% | high |
| Composite-Unseen | target | PortionHotDogs | 5 | 4 | 1 | 0 | 80.00% | high |
| Composite-Unseen | target | RecycleBottlesByType | 5 | 4 | 1 | 0 | 80.00% | high |
| Composite-Unseen | target | SeparateFreezerRack | 5 | 0 | 5 | 0 | 0.00% | high |
| Composite-Unseen | target | WaffleReheat | 5 | 1 | 4 | 0 | 20.00% | high |
| Composite-Unseen | target | WashFruitColander | 5 | 2 | 3 | 0 | 40.00% | high |
| Composite-Unseen | target | WeighIngredients | 5 | 1 | 4 | 0 | 20.00% | high |

---

## 第二部分 174 回合完整终局（批次 `202611031607`）

本项目整理能够从现存文件独立核查的 **GPT Direct 完整原生执行轨迹与结果**。发布范围共 174 回合，按任务子集和评估场景分别统计；其他位置保存的实验及仅有历史汇总的成绩不纳入本发布。

模型为 `gpt-6-astra`，推理强度为 `high`。控制实现属于论文引导的独立重建（paper-guided reconstruction），不宣称是原作者完整 RoboCasa 源码原样复现。

### 6. 结果汇总

| 子集 | 评估场景 | 有完整轨迹的任务数 | 成功／完整终局 | 完整终局子集 SR | 有记录任务宏平均 |
|---|---|---|---:|---:|---:|
| Atomic-Seen | pretrain-scene | 13 | 38/65 | 58.46% | 58.46% |
| Composite-Seen | pretrain-scene | 11 | 16/55 | 29.09% | 29.09% |
| Composite-Seen | target-scene | 15 | 10/54 | 18.52% | 15.11% |

这里“完整”指动作 ACK 覆盖全部实际物理步、原生 checker 覆盖初态至终态，并存在一致的 success 或 horizon 结果文件。图像按实际留存情况提供，不能把缺少历史 RGB 解释为已保存完整视觉输入。

Atomic-Seen pretrain 的 13 任务 65 回合与 Composite-Seen pretrain 的 11 任务 55 回合均完成其冻结名单，分别于 2026 年 10 月 19 日、10 月 22 日收尾；两者均不是相应子集全任务结果。pretrain-scene／target-scene 指**评估环境场景划分**，不表示训练数据范围。

#### 6.1 Composite-Seen target 的分母必须区分

历史 target 合同注册 16 任务、计划 58 回合，已接收 56 个策略结果。其中 54 条具有完整原生终局，另外两条是按原合同计失败的 `PolicyStop`（分别执行 20 步、0 步），还有 2 条未完成。

因此，本发布完整终局部分为 **10/54＝18.52%**，覆盖 15 个有完整轨迹的任务；原合同成绩仍为 **10/56＝17.86%**。两条 PolicyStop 没有作为完整轨迹打包，原合同成绩也没有被改写。18.52% 只是本次可发布完整终局部分的描述，不能据此宣称完整 58 回合评估已完成，或用筛掉提前停止来提高原合同成绩。

`StoreLeftoversInBowl` 没有可发布的完整原生终局，逐任务表中保留其缺项，不填 0% 成功率。target 各任务回合数不同，回合加权 SR 与有记录任务宏平均也不同。

### 7. 全部逐任务结果

#### 7.1 Atomic-Seen / pretrain-scene

| 任务 | 成功／完整终局 | 完整终局 SR | 原合同已接收 | 原合同 PolicyStop 失败 | 原合同待完成 | 物理步上限 H |
|---|---|---|---:|---:|---:|---:|
| CloseBlenderLid | 3/5 | 60.00% | 5 | 0 | 0 | 900 |
| CloseFridge | 5/5 | 100.00% | 5 | 0 | 0 | 900 |
| CloseToasterOvenDoor | 1/5 | 20.00% | 5 | 0 | 0 | 450 |
| NavigateKitchen | 5/5 | 100.00% | 5 | 0 | 0 | 450 |
| OpenCabinet | 3/5 | 60.00% | 5 | 0 | 0 | 1050 |
| PickPlaceCounterToCabinet | 3/5 | 60.00% | 5 | 0 | 0 | 750 |
| PickPlaceCounterToStove | 4/5 | 80.00% | 5 | 0 | 0 | 600 |
| PickPlaceToasterToCounter | 4/5 | 80.00% | 5 | 0 | 0 | 600 |
| SlideDishwasherRack | 2/5 | 40.00% | 5 | 0 | 0 | 450 |
| TurnOffStove | 4/5 | 80.00% | 5 | 0 | 0 | 750 |
| TurnOnElectricKettle | 2/5 | 40.00% | 5 | 0 | 0 | 450 |
| TurnOnMicrowave | 1/5 | 20.00% | 5 | 0 | 0 | 450 |
| TurnOnSinkFaucet | 1/5 | 20.00% | 5 | 0 | 0 | 600 |

#### 7.2 Composite-Seen / pretrain-scene

| 任务 | 成功／完整终局 | 完整终局 SR | 原合同已接收 | 原合同 PolicyStop 失败 | 原合同待完成 | 物理步上限 H |
|---|---|---|---:|---:|---:|---:|
| GetToastedBread | 1/5 | 20.00% | 5 | 0 | 0 | 3000 |
| LoadDishwasher | 2/5 | 40.00% | 5 | 0 | 0 | 1800 |
| PreSoakPan | 2/5 | 40.00% | 5 | 0 | 0 | 2400 |
| PrepareCoffee | 0/5 | 0.00% | 5 | 0 | 0 | 1800 |
| RinseSinkBasin | 0/5 | 0.00% | 5 | 0 | 0 | 1350 |
| ScrubCuttingBoard | 2/5 | 40.00% | 5 | 0 | 0 | 1200 |
| SetUpCuttingStation | 0/5 | 0.00% | 5 | 0 | 0 | 2400 |
| StackBowlsCabinet | 3/5 | 60.00% | 5 | 0 | 0 | 2100 |
| SteamInMicrowave | 0/5 | 0.00% | 5 | 0 | 0 | 2100 |
| StirVegetables | 5/5 | 100.00% | 5 | 0 | 0 | 2400 |
| StoreLeftoversInBowl | 1/5 | 20.00% | 5 | 0 | 0 | 2550 |

#### 7.3 Composite-Seen / target-scene

| 任务 | 成功／完整终局 | 完整终局 SR | 原合同已接收 | 原合同 PolicyStop 失败 | 原合同待完成 | 物理步上限 H |
|---|---|---|---:|---:|---:|---:|
| DeliverStraw | 1/5 | 20.00% | 5 | 0 | 0 | 2550 |
| GetToastedBread | 0/3 | 0.00% | 3 | 0 | 0 | 3000 |
| KettleBoiling | 4/5 | 80.00% | 5 | 0 | 0 | 1500 |
| LoadDishwasher | 0/3 | 0.00% | 3 | 0 | 0 | 1800 |
| PackIdenticalLunches | 1/5 | 20.00% | 5 | 0 | 0 | 3900 |
| PreSoakPan | 0/3 | 0.00% | 3 | 0 | 0 | 2400 |
| PrepareCoffee | 1/3 | 33.33% | 3 | 0 | 0 | 1800 |
| RinseSinkBasin | 0/3 | 0.00% | 3 | 0 | 0 | 1350 |
| ScrubCuttingBoard | 1/3 | 33.33% | 3 | 0 | 0 | 1200 |
| SearingMeat | 2/5 | 40.00% | 5 | 0 | 0 | 4350 |
| SetUpCuttingStation | 0/3 | 0.00% | 3 | 0 | 0 | 2400 |
| StackBowlsCabinet | 0/3 | 0.00% | 3 | 0 | 0 | 2100 |
| SteamInMicrowave | 0/3 | 0.00% | 3 | 0 | 0 | 2100 |
| StirVegetables | 0/2 | 0.00% | 3 | 1 | 0 | 2400 |
| StoreLeftoversInBowl | 0/0 | — | 1 | 1 | 2 | 2550 |
| WashLettuce | 0/5 | 0.00% | 5 | 0 | 0 | 1650 |

### 8. 轨迹完整性和图像可用性

| 子集 | 场景 | 完整执行轨迹 | 保有 RGB 的回合 | RGB 文件数 | 动作账本齐备 | 原生检查齐备 |
|---|---|---|---:|---:|---:|---:|
| Atomic-Seen | pretrain-scene | 65 | 65 | 5409 | 65 | 65 |
| Composite-Seen | pretrain-scene | 55 | 55 | 16635 | 55 | 55 |
| Composite-Seen | target-scene | 54 | 0 | 0 | 54 | 54 |

逐回合文件可用性、导出文件和 SHA 均有机器可读索引。较早的 target 迁移资料已裁去多数已完成回合的 RGB；本发布不补画面、不以重建图像冒充原始输入。

- 每条发布轨迹的动作 ACK 必须严格覆盖第 1 步至实际终止步，checker 必须覆盖第 0 步至终止步。
- 原生成功标签必须与结果文件、动作末态和 checker 末态一致；API 或工具返回成功不作为任务成功。
- 迁移副本和断点续跑接收快照去重，不重复增加统计分母；工程、基础设施失败和中断 attempt 不进入正式发布轨迹。
- 失败回合完整保留，不按成功挑选；两条 PolicyStop 只在原合同口径中保留说明。
- 不同场景的任务覆盖及初态分布不同，不能仅据 SR 差值声称场景的因果效应。
- 本包不将 π0.5、GR00T、恢复分支、教师标签、路由或事后 oracle 作为 GPT Direct 结果。部分历史用量未知，不按 0 费用处理。

### 9. 下载与使用

全部离线工具只使用 Python 标准库，不需要 GPU 或模型 API。

#### 9.1 下载项目并重算 SR

```bash
git clone https://github.com/Sam666-ai/RoboCasa365_v1.0.1-GPT6AstraDirect_Eval.git
cd RoboCasa365_v1.0.1-GPT6AstraDirect_Eval
python3 scripts/202611031607_重算成功率.py
```

也可选择 GitHub 项目页面 **Code → Download ZIP**，解压后在项目根目录运行上述 Python 命令。程序按逐回合结果重算三个子集／场景分组，并与随包冻结统计比较，正常时输出 `PASS`。

#### 9.2 下载完整轨迹、校验和解压

```bash
gh release download direct-trajectories-20261103 \
  --repo Sam666-ai/RoboCasa365_v1.0.1-GPT6AstraDirect_Eval \
  --pattern "*.tar.gz" --dir release_assets
python3 scripts/202611031607_校验下载与安全解压.py
python3 scripts/202611031607_校验下载与安全解压.py --extract
```

也可从 Releases 页面手动下载该版本的全部轨迹分包，放入项目的 `release_assets/` 目录。分包不需要手工拼接；工具逐包验证 SHA、逐文件 SHA 及 174 条原生结果，再安全解压到 `trajectories/`。只核对仓库内说明、统计及脚本时使用 `--core-only`。

#### 9.3 查看一个回合

```python
import csv, json
from pathlib import Path
root = Path(".")
catalog = next((root / "statistics").glob("*_逐回合结果索引.csv"))
episodes = list(csv.DictReader(catalog.open()))
episode = episodes[0]
folder = root / episode["trace_prefix"]
result = json.loads((folder / "episode_result.json").read_text())
print(episode["episode_id"], result["task"], result["native_success"])
```

`tools.jsonl` 记录观察／动作请求及动作理由；`agent_events.jsonl` 记录已保存的 agent 消息和操作事件；`evaluator/native_actions.jsonl` 是逐物理步动作与 ACK；`native_checker.jsonl` 记录原生成功检查。现存观察与 RGB 位于 `observation/`。

### 10. 文件结构与公开处理

```text
Readme.md
catalog/        # 批次 202611031026：子集/场景、逐任务 SR、历史 run 状态与来源缺口
manifests/      # 批次 202611031026：每个归档文件的大小、源 SHA、公开副本 SHA
reports/        # 批次 202611031026：完整性验收、链接闭包与原件缺口
tools/          # 批次 202611031026：分卷校验工具
statistics/     # 批次 202611031607：子集/场景、逐任务和逐回合结果
metadata/       # 批次 202611031607：版本、完整性、可用性、分包与 SHA 索引
scripts/        # 批次 202611031607：SR 重算、文件校验和安全解压
docs/           # 批次 202611031607：全部 174 回合结果表
release_assets/ # 解压/下载后的轨迹分包（不入 Git）
trajectories/   # 解压后生成（不入 Git）
```

部署路径、账户及服务身份已清理；动作数值、原生检查与成功标签保持。文件索引分别列出来源内容 SHA 和公开内容 SHA，在发生清理时两者可以不同。初态数组与 XML 作为归档证据保存；XML 资产路径已经清理，不能直接当作任意机器可恢复的仿真 checkpoint。

本项目分发任务级轨迹与现存 RGB，不分发重复 RPC 传输流、运行时数据库、服务配置、凭据、模型权重或仿真资产。这里的命令用于离线分析和统计复核，不启动在线实验；从零重跑仍需配置相应版本的 RoboCasa、资产、原生控制接口及模型服务。

---

## 附录 校验与已知限制

- 两批数据均按原始文件逐项计算 SHA256，公开副本与源文件分别记录 `source_sha256` 与 `public_sha256`，两者不同表示该文件经过已记录的敏感信息清理。
- 批次 `202611031026`：`python tools/verify_archive.py --payload` 可对全部分卷做逐文件校验；`publication_index.json` 中的 `status` 与逐卷 SHA 为准。
- 批次 `202611031607`：`scripts/202611031607_校验下载与安全解压.py` 逐包验证 SHA 与 174 条原生结果，可用 `--core-only` 只核对仓库内容。
- 未提供额外“全量交付 ZIP”：轨迹已由上述分包完整覆盖，重复打包只会增加体积。
- 本仓库不含模型权重、仿真资产、凭据或运行时数据库；也不构成任何在线服务的部署说明。
- 引用 SR 时必须同时写明批次号、子集/场景与分母口径；两批之间不做合并统计。
