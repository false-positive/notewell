import { Parser, HtmlRenderer } from 'commonmark';
import DOMPurify from 'dompurify';

export const mdToHtml = (md: string) => {
    const parser = new Parser();
    const writer = new HtmlRenderer();
    const parsedMd = parser.parse(md);
    const dangerousHtml = writer.render(parsedMd);
    const safeHtml = DOMPurify.sanitize(dangerousHtml);
    return safeHtml;
};
