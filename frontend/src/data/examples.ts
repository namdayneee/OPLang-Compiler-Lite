export interface CompilerExample {
  id: string
  name: string
  description: string
  expectedStage: 'codegen' | 'parser' | 'semantic'
  source: string
}

export const compilerExamples: readonly CompilerExample[] = [
  {
    id: 'hello-world',
    name: 'Hello World',
    description: 'Compile a minimal program that writes an integer.',
    expectedStage: 'codegen',
    source: `class Main {
    static void main() {
        io.writeIntLn(10);
    }
}`
  },
  {
    id: 'variables-arithmetic',
    name: 'Variables & Arithmetic',
    description: 'Declare local variables and compile an arithmetic expression.',
    expectedStage: 'codegen',
    source: `class Main {
    static void main() {
        int left := 20, right := 22;
        io.writeIntLn(left + right);
    }
}`
  },
  {
    id: 'if-else',
    name: 'If / Else',
    description: 'Compile a conditional statement with two branches.',
    expectedStage: 'codegen',
    source: `class Main {
    static void main() {
        if 2 < 3 then {
            io.writeIntLn(1);
        } else {
            io.writeIntLn(0);
        }
    }
}`
  },
  {
    id: 'for-loop',
    name: 'For Loop',
    description: 'Accumulate the integers from one through three.',
    expectedStage: 'codegen',
    source: `class Main {
    static void main() {
        int i := 0, sum := 0;
        for i := 1 to 3 do {
            sum := sum + i;
        }
        io.writeIntLn(sum);
    }
}`
  },
  {
    id: 'syntax-error',
    name: 'Syntax Error',
    description: 'Demonstrate a parser error caused by an incomplete class.',
    expectedStage: 'parser',
    source: 'class Main {'
  },
  {
    id: 'semantic-error',
    name: 'Semantic Error',
    description: 'Demonstrate an assignment to an undeclared identifier.',
    expectedStage: 'semantic',
    source: `class Main {
    static void main() {
        missing := 10;
    }
}`
  }
]
