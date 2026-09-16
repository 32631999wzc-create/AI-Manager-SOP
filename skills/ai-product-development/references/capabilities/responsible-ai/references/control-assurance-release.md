# Control Assurance and Release

## Use

当风险已识别，需要证明控制有效、定义发布条件、生产监控、事件处置和重评触发器时读取。

## Procedure

1. 将每个高/中风险连接到 `prevent | detect | contain | recover | remedy` 控制及 owner；声明控制覆盖不到的残余风险。
2. 把控制转换为 deterministic test、adversarial eval、人工演练或流程审查；记录被测版本、case、结果和限制。
3. 发布条件至少说明允许的人群/用例/权限/流量、必须通过的 guardrail、风险接受者和未满足时的 block/降级路径。
4. 生产监控关注伤害前兆、严重 bad case、权限异常、敏感数据和申诉，而不只监控服务 uptime。
5. 事件路径定义 `detect → contain → assess → correct → verify → communicate → remedy → learn`，并明确暂停、撤销权限或回滚的执行者。
6. 为模型、数据、权限、用例、人群、法规和控制变化设置重评条件；命中时生成 EvidenceRecord 并重新打开 DecisionRecord。

## Completion

关键控制有测试证据，残余风险由有权限者接受或阻塞，发布与事件路径可执行，监控和重评触发器连接明确 owner。
