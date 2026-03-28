# drelyx/proto

`drelyx/proto` is the source of truth for Drelyx gRPC contracts. The repository defines shared contracts for the panel, agent, and plugin SDK surface, then generates Go and TypeScript artifacts from the same schema.

## Layout

```text
proto/
├── proto/
│   ├── agent/v1/
│   ├── common/v1/
│   ├── panel/v1/
│   └── plugin/v1/
├── gen/
│   ├── go/
│   └── ts/
├── buf.gen.yaml
├── buf.yaml
├── Makefile
└── README.md
```

## Packages

- `drelyx.common.v1`: shared enums and reusable messages such as `ServerState`, `ResourceUsage`, `ServerConfig`, `AgentInfo`, and `Error`.
- `drelyx.agent.v1`: panel-to-agent RPCs for lifecycle control, console access, file operations, metrics, and status.
- `drelyx.panel.v1`: agent-to-panel reporting RPCs for telemetry, events, and crash reports.
- `drelyx.plugin.v1`: sidecar plugin stream contract for runtime events and acknowledgements.

## Generate Code

Prerequisites:

- `buf` on your `PATH`
- network access to fetch Buf dependencies and remote plugins

Generate all code:

```bash
make generate
```

Lint the schema:

```bash
make lint
```

`make generate` refreshes `buf.lock`, clears `gen/go` and `gen/ts`, and regenerates both SDK targets from the current schema.

## Go Usage

Generated Go packages live under `github.com/drelyx/proto/gen/go/...`.

Examples:

```go
import (
	agentv1 "github.com/drelyx/proto/gen/go/agent/v1"
	commonv1 "github.com/drelyx/proto/gen/go/common/v1"
	panelv1 "github.com/drelyx/proto/gen/go/panel/v1"
	pluginv1 "github.com/drelyx/proto/gen/go/plugin/v1"
)
```

Concrete import paths:

- `github.com/drelyx/proto/gen/go/agent/v1`
- `github.com/drelyx/proto/gen/go/common/v1`
- `github.com/drelyx/proto/gen/go/panel/v1`
- `github.com/drelyx/proto/gen/go/plugin/v1`

## TypeScript Usage

Generated TypeScript files live under `gen/ts/...` and are produced by the Buf-hosted `bufbuild/es` plugin. The generated code depends on:

- `@bufbuild/protobuf`
- `@connectrpc/connect`

Examples:

```ts
import { StartRequest } from "@drelyx/proto/gen/ts/agent/v1/agent_pb";
import { PluginService } from "@drelyx/proto/gen/ts/plugin/v1/plugin_pb";
import { ServerState } from "@drelyx/proto/gen/ts/common/v1/types_pb";
```

If this repository is consumed directly in a monorepo instead of through a published package, import from the relative generated path under `gen/ts`.

## Breaking Change Policy

The schema is versioned by package directory (`v1`) and guarded by Buf breaking checks.

- `buf.yaml` uses `STANDARD` lint rules.
- `buf.yaml` uses Buf's `WIRE` breaking policy, which is the wire-compatible guardrail for Protobuf binary compatibility.
- Never reuse or renumber removed fields.
- Reserve deleted field numbers and names before removing them from a message.
- Add new fields with new numbers only, and prefer additive changes over mutation.
- Introduce `v2` packages instead of breaking `v1` once wire compatibility cannot be preserved.

In practice, any contract change should run `make lint` and a Buf breaking comparison in CI against the previous mainline schema before release.
