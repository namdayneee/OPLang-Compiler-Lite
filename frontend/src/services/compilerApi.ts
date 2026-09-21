import type { CompilationResult } from '../types/compiler'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function compileSource(source: string): Promise<CompilationResult> {
  const response = await fetch(`${API_URL}/api/v1/compile`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      source,
      options: { includeAst: true, includeJasmin: true }
    })
  })

  if (!response.ok) {
    let message = `HTTP ${response.status}`
    try {
      const body = await response.json()
      message = body.detail ?? message
    } catch {
      // keep fallback
    }
    throw new Error(message)
  }

  return response.json()
}
