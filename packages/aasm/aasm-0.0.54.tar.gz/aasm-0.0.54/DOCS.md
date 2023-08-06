# Agents Assembly

## Table of Contents

- [Type Annotation Definitions](#type-annotation-definitions)
- [Preprocessor](#preprocessor)
  - [Makros](#preprocessor-makros)
  - [Constants](#preprocessor-constants)
- [Scope Modifiers](#scope-modifiers)
  - [Agent](#scope-modifiers-agent)
  - [Behavior](#scope-modifiers-behavior)
  - [Action](#scope-modifiers-action)
  - [Message](#scope-modifiers-message)
  - [Graph](#scope-modifiers-graph)
- [Agent Scope](#agent-scope)
  - [Parameters](#agent-scope-parameters)
- [Action Scope](#action-scope)
  - [Modifiers](#action-scope-modifiers)
  - [Math Expressions](#action-scope-math-expressions)
  - [Conditional Statements](#action-scope-conditional-statements)
  - [Loops](#action-scope-loops)
  - [Lists](#action-scope-lists)
  - [Miscellaneous](#action-scope-miscellaneous)
- [Message Scope](#message-scope)
  - [Parameters](#message-scope-parameters)
- [Graph Scope](#graph-scope)
  - [Parameters](#graph-scope-parameters)


## Type Annotation Definitions <a name = "type-annotation-definitions"></a>

`{...}` - One of the options from the brackets needs to be chosen, written as specified within the brackets.

`[...]` - Optional arguments.

`Name` - A unique sequence of alphanumeric characters which does not contain any forbidden symbols and does not begin with a number. Some instructions put further restrictions on `Name`s.

`Float` - A floating-point number or variable.

`MutFloat` - A floating-point variable with the possibility of being modified.

`Integer` - An integer. If a `Float` is passed as an argument of this type, it will be rounded.

`Enum` - An enumerable that stores a state in the form of `EnumVal`.

`EnumVal` - A distinct enumerable state.

`Message` - A message defined using the `MESSAGE` instruction.

`Jid` - Agent identifier. Literals start and end with `"`. For example, `"text@example.com"`.

`ACLPerformative` - One of the FIPA-defined ACL performative types.

`DistArgs` - Arguments for a specified distribution. Mathematical constraints apply.

## Preprocessor <a name = "preprocessor"></a>
Preprocessor directives begin with `%`.

### Makros <a name = "preprocessor-makros"></a>
Makros can be used to reduce repetitive code or improve readability. When called, they expand in-place the definition by substituting makro arguments for call parameters.

*Example usage:*
```aasm
%MAKRO add_if_greater_else val1, val2, flag
  SET flag, 0
  IGT val1, val2
    ADD val1, 1
    SET flag, 1
  EBLOCK
  ILTEQ val1, val2
    IEQ flag, 1
      ADD val2, 1
    EBLOCK
  EBLOCK
%EMAKRO

# ...omitted

ACTION hello, modify_self
  DECL flag, float 0
  add_if_greater_else param1, param2, flag
EACTION
```
### Constants <a name = "preprocessor-constants"></a>
They are used to define globally set numbers. They can be used in all scopes (including agent and message params and network definition).

*Example usage:*
```aasm
%CONST sim_size, 10000

# ...omitted

AGENT manager
  PRM alive, float, init, sim_size
EAGENT
```

## Scope Modifiers <a name = "scope-modifiers"></a>

### Agent <a name = "scope-modifiers-agent"></a>
`AGENT name: Name` - Enters the scope for describing an agent.

`EAGENT` - Exists agent scope. It has to correspond to `AGENT`.

*Example usage:*
```aasm
AGENT
  # agent definition here
EAGENT
```

### Behavior <a name = "scope-modifiers-behavior"></a>
`BEHAV name: Name, type: {setup, one_time, cyclic, msg_rcv} [, b_args]` - Enters scope for describing a Behaviour of specified `type`. `b_args` depend on the specified `type`. The name is required to be unique within `AGENT` scope. It can only be used within `AGENT` scope.

Behavior types:
 * `setup` - Fires on setup, no additional arguments are used.
 * `one_time` (`b_args` is `delay: Float`) - Fires after `delay` seconds. `delay` must be greater than `0`.
 * `cyclic` (`b_args` is `period: Float`) - Fires every `period` seconds. `period` must be greater than `0`.
 * `msg_rcv` (`b_args` is `msg_name: Name, msg_type: ACLPerformative`) - Fires upon receiving message matching name `msg_name` and `msg_type`.

`EBEHAV` - Exists behavior scope. It has to correspond to `BEHAV`.

*Example usage:*
```aasm
BEHAV read_message, msg_rcv, test_message, inform
  # behavior definition
EBEHAV
```

### Action <a name = "scope-modifiers-action"></a>
`ACTION name: Name, type: {modify_self, send_msg}` - Enters scope for describing an Action of the specified `type`. The name is required to be unique within the `BEHAV` scope. It can only be used within the `BEHAV` scope.

`EACTION` - Exists action scope. It has to correspond to `ACTION`.

*Example usage:*
```aasm
ACTION add_friend, modify_self
  # action definition
EACTION
```

### Message <a name = "scope-modifiers-message"></a>
`MESSAGE name: Name, performative: ACLPerformative` - Enters the scope for describing a Message of the specified name and performative.

`EMESSAGE` - Exists message scope. It has to correspond to `MESSAGE`.

*Example usage:*
```aasm
MESSAGE test_message, inform
  # message definition
EMESSAGE
```

### Graph <a name = "scope-modifiers-graph"></a>
`GRAPH type: {statistical}` - Enters the scope for creation of a graph of specified `type`.

`EGRAPH` - Exists graph scope. It has to correspond to `GRAPH`.

*Example usage:*
```aasm
GRAPH statistical
  # graph definition
EGRAPH
```

## Agent Scope <a name = "agent-scope"></a>

### Parameters <a name = "agent-scope-parameters"></a>
`PRM name: Name, type: {float, enum, list}, subtype: {init, dist, conn, msg} [, p_args]` - Creates an agent parameter of specified type and subtype. Describes the initial state of an agent by passing arguments `p_args`.

Types:
 * `float`
   * `init` (`p_args` is `val: Float`) - Creates a float parameter. Value `name` is set to `val` during agent initiation.
   * `dist` (`p_args` is `dist: {normal, uniform, exp}, dist_args: DistArgs`) - Creates a float parameter. Value `name` is set to a value drawn from specified `dist` distribution.
 * `enum` (`p_args` is `val1, val1%, ..., valn, valn%`) - Creates an enum parameter. Value `name` is set to one of `val1, ... ,valn`. Corresponding `vali%` arguments specify the percentage of the total agent population to have a specific value set on startup.
 * `list`
   * `conn` - Creates a connection list parameter. List is empty on startup.
   * `msg` - Creates a message list parameter. List is empty on startup.

## Action Scope <a name = "action-scope"></a>

### Modifiers <a name = "action-scope-modifiers"></a>

`DECL name: Name, type: {float, conn} value: Float/Jid` - Creates a variable of specified `type` with `name` and `value`. The new variable can only be used in given action's scope.

`SET dst: MutFloat/Enum, value: Float/EnumVal` - Sets value of `dst` to `value`.

`SUBS dst: List, src: List, num: Integer` - Chooses `num` elements from `src` and sets `dst` to them.

### Math Expressions <a name = "action-scope-math-expressions"></a>

`ADD dst: MutFloat, arg: Float` - Adds `arg` to `dst` and stores result in `dst`.

`MULT dst: MutFloat, arg: Float` - Multiplies `arg` by `dst` and stores result in `dst`.

`SUBT dst: MutFloat, arg: Float` - Subtracts `arg` from `dst` and stores result in `dst`.

`DIV dst: MutFloat, arg: Float` - Divides `arg` by `dst` and stores result in `dst`. If `arg` is `0` then the `ACTION` will finish early.

`SIN dst: MutFloat, arg: Float` - Calculates the sine of `arg` radians and stores it in `dst`.

`COS dst: MutFloat, arg: Float` - Calculates the cosine of `arg` radians and stores it in `dst`.

`POW dst: MutFloat, base: Float, arg: Float` - Calculates `base` raised to `arg` power and stores the result in `dst`.

`LOG dst: MutFloat, base: Float, arg: Float` - Calculcates `base` logarithm of `arg` and stores the result in `dst`.

`MOD dst: MutFloat, dividend: Float, divisor: Float` - Calculcates `dividend` mod `divisor` and stores the result in `dst`.

### Conditional Statements <a name = "action-scope-conditional-statements"></a>
`IEQ a: Float/Enum, b: Float/EnumVal` - Begins conditional block if `a` is equal to `b`. Needs matching `EBLOCK`.

`INEQ a: Float/Enum, b: Float/EnumVal` - Begins conditional block if `a` is not equal to `b`. Needs matching `EBLOCK`.

`ILT a: Float, b: Float` - Begins conditional block if `a` is less than `b`. Needs matching `EBLOCK`.

`IGT a: Float, b: Float` - Begins conditional block if `a` is greater than `b`. Needs matching `EBLOCK`.

`ILTEQ a: Float, b: Float` - Begins conditional block if `a` is less or equal `b`. Needs matching `EBLOCK`.

`IGTEQ a: Float, b: Float` - Begins conditional block if `a` is greater or equal `b`. Needs matching `EBLOCK`.

### Loops <a name = "action-scope-loops"></a>
`WEQ a: Float/Enum, b: Float/EnumVal` - Begins loop block if `a` is equal to `b`. Needs matching `EBLOCK`.

`WNEQ a: Float/Enum, b: Float/EnumVal` - Begins loop block if `a` is not equal to `b`. Needs matching `EBLOCK`.

`WLT a: Float, b: Float` - Begins loop block if `a` is less than `b`. Needs matching `EBLOCK`.

`WGT a: Float, b: Float` - Begins loop block if `a` is greater than `b`. Needs matching `EBLOCK`.

`WLTEQ a: Float, b: Float` - Begins loop block if `a` is less or equal `b`. Needs matching `EBLOCK`.

`WGTEQ a: Float, b: Float` - Begins loop block if `a` is greater or equal `b`. Needs matching `EBLOCK`.

### Lists <a name = "action-scope-lists"></a>

`ADDE list: List, value: Message/Jid` - Adds `value` to `list`.

`REME list: List, value: Message/Jid` - Removes `value` from `list`. If `value` is not in the list, does nothing.

`REMEN list: List, num, Integer` - Removes `num` random elements from `list`. If `list` is too short, it clears it.

`LEN result: MutFlost, list: List` - Saves length of `list` in `result`.

`CLR list: List` - Clears contents of `list`.

`IN list: List, value: Message/Jid` - Begins conditional block if `val` is in `list`. Needs matching `EBLOCK`.

`NIN list: List, value: Message/Jid` - Begins conditional block if `val` is not in `list`. Needs matching `EBLOCK`.

`SUBS dst: List, src: List, num: Float` - Takes `num` randomly selected elements of `src` and stores them in `dst`.

`LW dst: List, val: Float/Jid, idx: Float` - Writes `val` at index `idx` of `dst`.

`LR dst: Float/Jid, src: List, idx: Float` - Reads value from list `src` at index `idx` and stores it in `dst`.

### Miscellaneous <a name = "action-scope-miscellaneous"></a>
`EBLOCK` - Ends current conditional or loop block.

`SEND rcv: ConnList/Jid` - Sends message to `rcv`. Can only be used inside `send_msg` actions.

`RAND result: MutFloat, cast: {float, int}, dist: {uniform, normal, exp}, dist_args: DistArgs` - Stores a value drawn from specified `dist` distribution, casts it to `cast` type and stores it in `result`.

`.` (`msg.prm`) - Allows to access the value of `prm` from `msg`.

## Message Scope <a name = "message-scope"></a>

### Parameters <a name = "message-scope-parameters"></a>
`PRM name: Name, type: {float, conn}` - Creates a new message parameter of specified type. `name` cannot be "sender", "type", or "performative".

## Graph Scope <a name = "graph-scope"></a>

### Parameters <a name = "graph-scope-parameters"></a>
`SIZE value: Integer` - Sets the size of the graph.

`DEFG agent_type: Name, amount: Float[%], connections: {Float, dist_normal, dist_uniform, dist_exp} [, DistArgs]` - Creates a new agent type with specified `amount` of agents and number `connections`. If the `amount` ends with `%`, then the percent refers to the size of the graph; else, it does not respect the size of the graph. The number of connections can be specified as a number or distribution. In the case of a fixed number, each agent will have the same number of connections. In the case of a distribution, each agent will have the number of connections drawn from the distribution.
