# Acquisition security boundary

Acquisition handles hostile external input. It is not a trusted execution environment.

Required controls for concrete connectors:

- allow only HTTP(S) unless an explicit source policy permits another mechanism;
- reject URL userinfo and embedded credentials;
- reject literal loopback, private, link-local, multicast, reserved, and unspecified IPs;
- resolve DNS and re-check the selected address immediately before connection;
- revalidate every redirect destination;
- never forward source credentials across origins;
- enforce maximum response bytes, decompression expansion, header size, timeout, and redirect limits;
- persist raw bytes before semantic parsing;
- parse untrusted formats in isolated workers/processes;
- never execute fetched content;
- never pass raw remote content to privileged agent/tool execution;
- treat prompt-injection text as untrusted data.

The Phase 1 Python helper intentionally implements only deterministic URL preflight.
DNS rebinding, connection-time policy, and resource limits belong to the concrete network adapter.
