# GPT6Astra Direct · RoboCasa365 本机轨迹归档

文档生成时间：2026-11-03 10:59（北京时间）。

## 1. 本机已找到的基线范围与 SR

| RoboCasa365 子集 | scene | 任务数 | 接纳记录 | 原生完整记录 | 成功 | 原生失败 | 提前停止 | micro SR |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Composite-Unseen | pretrain | 11 | 55 | 55 | 26 | 29 | 0 | 47.27% |
| Composite-Seen | target | 16 | 57 | 55 | 10 | 45 | 2 | 18.18% |
| Composite-Unseen | target | 16 | 80 | 80 | 37 | 43 | 0 | 46.25% |

合计 **192 条接纳记录，190 条原生完整记录，73 条成功**。这里“原生完整”指 native success，或未被基础设施标为无效且实际执行达到原生 horizon；流程层 `status=complete` 并不自动表示原生完整。表内 SR = 成功数 / 原生完整记录数。

Composite-Seen/target 原计划 58 条，当前接纳 57 条；其中 2 条 policy/其他提前停止不计入本表原生失败分母，另有 1 条缺失／基础设施问题。因此 18.18% 是 10/55，不能写作完成了全部计划、也不能默默把早停算作原生失败。若按接纳记录把早停计失败，结果为 10/57=17.54%；按计划 58 条的完成情况应另行报告。

Composite-Unseen/pretrain 的 reasoning effort 混有 `high` 与 `xhigh`，逐记录原值保留；另外两组为 `high`。实际模型标识见原始结果及索引，不能把本批概括为统一 effort 的新控制实验。

三个最终接纳面板按原始输出目录去重，不能累加历史续跑目录中继承的 `ACCEPTED_RESULTS.json`。39 个主 run 目录共找到 **277 个 `episode_result.json`**，其中还包含重试、基础设施失败、smoke 与开发记录；它们不等于 277 条独立正式基线。只有状态而没有结果文件的中断尝试仍在原始归档中，277 也不是历史尝试总数的保证。

以下两组目前只有异机导入的成绩参考，**没有找到本机原始轨迹**：Atomic-Seen/pretrain（65 条，38 成功）、Composite-Seen/pretrain（55 条，16 成功）。相关历史表／报告保留为来源参考，不计作本包本机 rollout；没有声称本机存在 Atomic target 的 Direct 基线。

## 2. 数据分卷

```text
202611031026H_A_GPT6AstraDirect全子集轨迹归档/
├── Readme.md              # 本说明的便捷副本
├── github/                # 这一层的内容作为 GitHub 仓库根目录
│   ├── Readme.md
│   ├── .gitignore
│   ├── publication_index.json
│   ├── catalog/           # 子集/scene、逐任务 SR、历史run状态与来源缺口
│   ├── manifests/         # 每个归档文件的大小、源 SHA、公开副本 SHA
│   ├── reports/           # 文件完整性验收、链接闭包和原件缺口
│   └── tools/verify_archive.py
├── archives/              # 大体积轨迹分卷；上传到 GitHub Release
├── <时间戳>H_A_GitHub说明索引与校验清单.zip
├── <时间戳>H_A_SHA256SUMS.txt
└── work/                  # 私有构建中间件、源路径映射及旧不完整尝试，不上传
```

五组数据如下。分卷文件名均为 `202611031026H_A_GPT6AstraDirect_<组名>.tar.zst.partNNN`。

| 组名 | 内容 | 文件数 | 原始字节量 GB | 压缩后 GB | 分卷数 |
|---|---|---:|---:|---:|---:|
| `CompositeUnseen_pretrain` | Unseen/pretrain 主线及早期重试/开发记录 | 69,502 | 18.571 | 11.948 | 6 |
| `CompositeSeen_target` | Seen/target 主线及重试/续跑记录 | 81,041 | 26.775 | 14.393 | 8 |
| `CompositeUnseen_target` | Unseen/target 主线及重试/续跑记录 | 90,543 | 24.266 | 15.258 | 8 |
| `references_and_early_diagnostics` | 历史 K1 Direct、冻结源码、复现工具与来源报告 | 2,945 | 4.684 | 4.224 | 3 |
| `link_closure` | 可找到的原 codex/agent 链接目标，转存为普通文件 | 1,730 | 0.235 | 0.228 | 1 |

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
├── historical_direct_with_perception/  # 早期K1工程/诊断，单独保留
├── reproduction_tools/
└── references/ …                       # 以逐文件manifest中的路径为准
```

不同历史 run 的布局有差异；全部真实相对路径以 `manifests/*.files.jsonl.gz` 为准。早期 K1 使用额外感知工具，不能和后期 Direct 基线合并报告 SR。

## 3. 如何找到并回看一次 rollout

先选对应子集／scene 的归档组，解包后在 `GPT6AstraDirect/runs/` 按任务目录查找。主线、开发、smoke、重试按原目录保留；最终接纳记录应使用下面三个最终 run 的原始 `ACCEPTED_RESULTS.json` 核对，清单中的本机绝对输出路径应改为解包后相应 `GPT6AstraDirect/runs/` 相对路径：

- Composite-Unseen/pretrain：`20261008T0818Z_reboot_serial_resume`。
- Composite-Seen/target：`20261016_seen_target_gpu3_retry42_resume`。
- Composite-Unseen/target：`20261026T181500Z_composite_unseen_target_harnesscl_coexist_resume8`。

查看 `episode_result.json` 的 `native_success`、`control_steps`、`horizon`、reasoning effort 与费用状态。三相机图像通常位于 `codex/agent/observations/request_*`，按请求编号顺序回看，并结合 `observation.json`、动作账本、环境回执及 RPC 判断实际执行过程。保存的是记录时的观测帧，不保证是连续 20 Hz 视频，也不保证每个历史中断都有全部图像。

费用记录保留原始用量与未知标记；`usage_complete=false` 或终局用量未知不能当作零成本。原始 `initial.xml`/状态数组的存在不表示已验证跨机器精确恢复；本次没有重放物理或重新验收任务成功语义。

## 4. 下载、校验与解包

从仓库 Release 下载所需数据组的**全部**分卷；建议同时下载 metadata ZIP 和 SHA256SUMS。仅回看一个子集可只取该数据组；为补齐 `codex/agent` 记录还应下载 `link_closure`。历史工具和报告位于 `references_and_early_diagnostics`。

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
sha256sum -c 202611031026H_A_SHA256SUMS.txt
```

上述 SHA 清单包含整个交付集，少下文件会报告缺失；选择性下载请使用 `--group`。全量下载并解包 metadata ZIP 后，可用 `--payload` 不加 `--group` 完整验真。

解包一个数据组的示例（先完成校验；在存放分卷的目录执行）：

```bash
mkdir -p data
cat 202611031026H_A_GPT6AstraDirect_CompositeUnseen_target.tar.zst.part* \
  | zstd -dc --memory=512MB | tar -xf - -C data
```

其余组依次替换组名，解到同一个 `data/` 即可。顺序固定的三位 part 编号可直接按文件名拼接。完整解包需要约 75 GB 文件内容空间，另预留文件系统开销；若同时保留下载分卷，还需加上压缩文件体积。没有 zstd 时先安装系统 `zstd`，不要把 part 当作 ZIP。

## 5. 完整逐任务结果

以下为这三组本机最终接纳面板的全部任务；不额外生成逐 seed 表。每任务可能因早停／缺项而样本数不相等，所以全体 micro SR 不能直接称为逐任务平均 SR。

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
