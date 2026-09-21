export type CompilerError = {
  stage: string
  code: string
  message: string
  line?: number | null
  column?: number | null
}

export type CompilationResult = {
  success: boolean
  stage: string
  ast: unknown | null
  jasmin_files: Record<string, string>
  errors: CompilerError[]
  compilation_time_ms: number
}
