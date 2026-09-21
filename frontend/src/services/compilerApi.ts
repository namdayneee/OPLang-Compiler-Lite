import type { CompilationResult, CompileOptions } from '../types/compiler'

const DEFAULT_API_URL = 'http://localhost:8000'
const API_URL = (import.meta.env.VITE_API_URL ?? DEFAULT_API_URL).replace(/\/$/, '')

type ApiErrorBody = {
  detail?: string | { message?: string }
}

function errorMessage(body: ApiErrorBody, fallback: string): string {
  if (typeof body.detail === 'string') return body.detail
  return body.detail?.message ?? fallback
}

export async function compileSource(
  source: string,
  options: CompileOptions,
  signal?: AbortSignal
): Promise<CompilationResult> {
  const response = await fetch(`${API_URL}/api/v1/compile`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      source,
      options
    }),
    signal
  })

  if (!response.ok) {
    const fallback = `Compiler API returned HTTP ${response.status}`
    let message = fallback
    try {
      const body = (await response.json()) as ApiErrorBody
      message = errorMessage(body, fallback)
    } catch {
      // The response may not contain JSON; retain the HTTP status fallback.
    }
    throw new Error(message)
  }

  return (await response.json()) as CompilationResult
}
