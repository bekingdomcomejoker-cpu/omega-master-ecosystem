import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter"
import { dracula } from "react-syntax-highlighter/dist/esm/styles/prism"

interface MarkdownRendererProps {
  content: string
  className?: string
}

export function MarkdownRenderer({ content, className = "" }: MarkdownRendererProps) {
  return (
    <div className={`prose prose-invert max-w-none ${className}`}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          // Headings
          h1: ({ children }) => (
            <h1 className="text-2xl font-bold text-cyan-400 mt-4 mb-2">{children}</h1>
          ),
          h2: ({ children }) => (
            <h2 className="text-xl font-bold text-cyan-300 mt-3 mb-2">{children}</h2>
          ),
          h3: ({ children }) => (
            <h3 className="text-lg font-bold text-cyan-200 mt-2 mb-1">{children}</h3>
          ),
          
          // Paragraphs
          p: ({ children }) => (
            <p className="text-zinc-300 mb-3 leading-relaxed">{children}</p>
          ),
          
          // Lists
          ul: ({ children }) => (
            <ul className="list-disc list-inside text-zinc-300 mb-3 space-y-1">{children}</ul>
          ),
          ol: ({ children }) => (
            <ol className="list-decimal list-inside text-zinc-300 mb-3 space-y-1">{children}</ol>
          ),
          li: ({ children }) => (
            <li className="text-zinc-300">{children}</li>
          ),
          
          // Code
          code: ({ inline, className: codeClassName, children, ...props }: any) => {
            const match = /language-(\w+)/.exec(codeClassName || "")
            const language = match ? match[1] : "text"
            
            if (inline) {
              return (
                <code className="bg-zinc-800 text-amber-300 px-2 py-1 rounded text-sm font-mono">
                  {children}
                </code>
              )
            }
            
            return (
              <div className="my-4 rounded-lg overflow-hidden">
                <SyntaxHighlighter
                  language={language}
                  style={dracula}
                  className="!bg-zinc-900 !m-0"
                  customStyle={{
                    fontSize: "0.875rem",
                    lineHeight: "1.5",
                    padding: "1rem"
                  }}
                >
                  {String(children).replace(/\n$/, "")}
                </SyntaxHighlighter>
              </div>
            )
          },
          
          // Blockquotes
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-purple-500 pl-4 py-2 my-3 text-purple-300 italic">
              {children}
            </blockquote>
          ),
          
          // Links
          a: ({ href, children }) => (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-cyan-400 hover:text-cyan-300 underline"
            >
              {children}
            </a>
          ),
          
          // Tables
          table: ({ children }) => (
            <div className="overflow-x-auto my-4">
              <table className="w-full border-collapse border border-purple-500/30">
                {children}
              </table>
            </div>
          ),
          thead: ({ children }) => (
            <thead className="bg-purple-900/30">{children}</thead>
          ),
          tbody: ({ children }) => (
            <tbody>{children}</tbody>
          ),
          tr: ({ children }) => (
            <tr className="border-b border-purple-500/20">{children}</tr>
          ),
          th: ({ children }) => (
            <th className="border border-purple-500/30 px-4 py-2 text-left text-cyan-300 font-semibold">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="border border-purple-500/30 px-4 py-2 text-zinc-300">
              {children}
            </td>
          ),
          
          // Horizontal rule
          hr: () => (
            <hr className="my-4 border-t border-purple-500/30" />
          ),
          
          // Emphasis
          em: ({ children }) => (
            <em className="italic text-zinc-200">{children}</em>
          ),
          strong: ({ children }) => (
            <strong className="font-bold text-cyan-300">{children}</strong>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
}
