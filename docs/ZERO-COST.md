# Zero-cost deployment guardrails

Goal: portfolio/demo operation with a cash cost of 0 VND, accepting free-tier service suspension instead of overage billing.

## GitHub

- Keep repository public.
- Use standard GitHub-hosted runners only.
- Do not select larger runners.

## Cloudflare Pages

- Use the generated `pages.dev` hostname.
- No paid domain is required.
- Avoid server-side Pages Functions in v1; frontend is static.

## Render

- Hobby workspace.
- Web Service compute plan: Free.
- Do not add a payment method if you want hard protection from usage charges.
- Accept idle spin-down/cold start.
- Accept service/build suspension if included usage is exhausted.

## Application architecture

- No PostgreSQL.
- No Redis.
- No persistent disk.
- No object storage.
- No paid monitoring service.
- No paid domain.
- Source stays in browser `localStorage`.
- Compiler work happens in ephemeral temporary directories.

## Monthly cash-cost target

```text
GitHub repo/actions      0 VND
Cloudflare Pages         0 VND
Render Free              0 VND
Database                 0 VND
Storage                  0 VND
Domain                   0 VND
TLS                      0 VND
Total                    0 VND
```

Free-tier limits and vendor policies can change, so re-check provider documentation before each public release.
