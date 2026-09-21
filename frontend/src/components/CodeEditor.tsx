import Editor from '@monaco-editor/react'

type Props = {
  value: string
  onChange: (value: string) => void
}

export function CodeEditor({ value, onChange }: Props) {
  return (
    <Editor
      height="70vh"
      defaultLanguage="java"
      theme="vs-dark"
      value={value}
      onChange={(next) => onChange(next ?? '')}
      options={{
        minimap: { enabled: false },
        fontSize: 14,
        automaticLayout: true,
        tabSize: 4,
        scrollBeyondLastLine: false
      }}
    />
  )
}
