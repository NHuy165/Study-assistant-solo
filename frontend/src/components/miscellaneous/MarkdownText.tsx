import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import remarkGfm from 'remark-gfm';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';

export const MarkdownText = ({
  content,
  style,
}: {
  content: string;
  style?: string;
}) => {
  return (
    <div
      className={`prose prose-p:my-0 prose-ul:my-0 prose-li:my-0 prose-heading:my-0 max-w-full ${style}`}
    >
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeKatex]}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};
