# Repository Guidelines

## Project Structure & Module Organization

This repository is the source of truth for Drelyx gRPC contracts.

- `proto/common/v1/`: shared enums and messages used across services.
- `proto/agent/v1/`: panel-to-agent RPC definitions.
- `proto/panel/v1/`: agent-to-panel reporting RPCs.
- `proto/plugin/v1/`: sidecar plugin streaming interface.
- `gen/go/` and `gen/ts/`: generated SDK outputs. Do not edit these by hand.
- `.github/workflows/`: CI and release automation.

When changing contracts, edit only files under `proto/` and then regenerate `gen/`.

## Build, Test, and Development Commands

- `make lint`: runs `buf lint` against the schema.
- `make generate`: regenerates `gen/go` and `gen/ts` from current proto files.
- `make deps`: refreshes `buf.lock` after dependency changes.
- `buf breaking --against '.git#branch=main'`: checks wire compatibility against `main`.

Typical workflow:

```bash
make lint
make generate
git diff -- gen
```

## Coding Style & Naming Conventions

- Use `proto3` syntax and keep package names versioned, for example `drelyx.agent.v1`.
- Keep field numbers stable. Never reuse removed field numbers; reserve them instead.
- Add comments for every message and important field.
- Use `oneof` for union-shaped payloads.
- IDs must be `string` values; timestamps must use `google.protobuf.Timestamp`.
- Generated code must come only from Buf; never patch files in `gen/`.

## Testing Guidelines

This repo does not use unit tests. Validation is schema-based:

- `make lint` must pass.
- `make generate` must produce no unexpected diffs.
- Breaking changes must be checked before merge, especially for `v1` packages.

If a schema change modifies generated files, include the updated `gen/` output in the same commit.

## Commit & Pull Request Guidelines

Follow the existing conventional commit style:

- `feat: define drelyx grpc contracts`
- `build: add buf toolchain and generated sdk outputs`
- `ci: add github actions for proto validation and releases`

Each commit should represent one logical change. Pull requests should include:

- a short summary of the contract change,
- whether it is additive or breaking,
- regenerated `gen/go` and `gen/ts` outputs,
- linked issue or design context when available.
