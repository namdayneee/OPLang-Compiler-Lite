export type CompilerStage =
  | 'lexer'
  | 'parser'
  | 'ast'
  | 'semantic'
  | 'codegen'

export interface CompilerError {
  stage: string
  code: string
  message: string
  line?: number | null
  column?: number | null
}

export interface CompileOptions {
  includeAst: boolean
  includeJasmin: boolean
}

export interface CompilationResult {
  success: boolean
  stage: CompilerStage
  ast: unknown | null
  jasmin_files: Record<string, string>
  errors: CompilerError[]
  compilation_time_ms: number
}
