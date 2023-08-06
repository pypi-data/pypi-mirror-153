/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { Global, PRE } from '../Global';

import { SxProps, Theme } from '@mui/system';

import { defaultSanitizer } from '@jupyterlab/apputils';

import escape from 'lodash.escape';

interface IProps {
    text: string
    sx?: SxProps<Theme>
}
interface IState {}

export class AnsiLink extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <PRE sx={Object.assign({}, this.props.sx)} dangerouslySetInnerHTML={{ __html: autolink(defaultSanitizer.sanitize(ansiSpan(this.props.text))) }} />
        )
    }
}

/// The functions below were taken from https://github.com/jupyterlab/jupyterlab/blob/b05c2748c021a8da681315fd0a6bcaee01e96d6b/packages/rendermime/src/renderers.ts

function autolink(content: string): string {
    // Taken from Visual Studio Code:
    // https://github.com/microsoft/vscode/blob/9f709d170b06e991502153f281ec3c012add2e42/src/vs/workbench/contrib/debug/browser/linkDetector.ts#L17-L18
    const controlCodes = '\\u0000-\\u0020\\u007f-\\u009f';
    const webLinkRegex = new RegExp(
        '(?:[a-zA-Z][a-zA-Z0-9+.-]{2,}:\\/\\/|data:|www\\.)[^\\s' +
        controlCodes +
        '"]{2,}[^\\s' +
        controlCodes +
        '"\'(){}\\[\\],:;.!?]',
        'ug'
    );
    return content.replace(webLinkRegex, url => {
        // Special case when the URL ends with ">" or "<"
        const lastChars = url.slice(-3);
        const endsWithGtLt = ['&gt', '&lt'].indexOf(lastChars) !== -1;
        const toAppend = endsWithGtLt ? lastChars : '';
        const len = endsWithGtLt ? url.length - 3 : url.length;
        return (
            `<a href="${url.slice(0, len)}" rel="noopener" target="_blank">` +
            `${url.slice(0, len)}</a>${toAppend}`
        );
    });
}

const ANSI_COLORS = [
    'ansi-black',
    'ansi-red',
    'ansi-green',
    'ansi-yellow',
    'ansi-blue',
    'ansi-magenta',
    'ansi-cyan',
    'ansi-white',
    'ansi-black-intense',
    'ansi-red-intense',
    'ansi-green-intense',
    'ansi-yellow-intense',
    'ansi-blue-intense',
    'ansi-magenta-intense',
    'ansi-cyan-intense',
    'ansi-white-intense'
];

/**
 * Create HTML tags for a string with given foreground, background etc. and
 * add them to the `out` array.
 */
function pushColoredChunk(
    chunk: string,
    fg: number | Array<number>,
    bg: number | Array<number>,
    bold: boolean,
    underline: boolean,
    inverse: boolean,
    out: Array<string>
): void {
    if (chunk) {
        const classes = [];
        const styles = [];

        if (bold && typeof fg === 'number' && 0 <= fg && fg < 8) {
            fg += 8; // Bold text uses "intense" colors
        }
        if (inverse) {
            [fg, bg] = [bg, fg];
        }

        if (typeof fg === 'number') {
            classes.push(ANSI_COLORS[fg] + '-fg');
        } else if (fg.length) {
            styles.push(`color: rgb(${fg})`);
        } else if (inverse) {
            classes.push('ansi-default-inverse-fg');
        }

        if (typeof bg === 'number') {
            classes.push(ANSI_COLORS[bg] + '-bg');
        } else if (bg.length) {
            styles.push(`background-color: rgb(${bg})`);
        } else if (inverse) {
            classes.push('ansi-default-inverse-bg');
        }

        if (bold) {
            classes.push('ansi-bold');
        }

        if (underline) {
            classes.push('ansi-underline');
        }

        if (classes.length || styles.length) {
            out.push('<SPAN');
            if (classes.length) {
                out.push(` class="${classes.join(' ')}"`);
            }
            if (styles.length) {
                out.push(` style="${styles.join('; ')}"`);
            }
            out.push('>');
            out.push(chunk);
            out.push('</SPAN>');
        } else {
            out.push(chunk);
        }
    }
}

/**
 * Convert ANSI extended colors to R/G/B triple.
 */
function getExtendedColors(numbers: Array<number>): number | Array<number> {
    let r;
    let g;
    let b;
    const n = numbers.shift();
    if (n === 2 && numbers.length >= 3) {
        // 24-bit RGB
        r = numbers.shift()!;
        g = numbers.shift()!;
        b = numbers.shift()!;
        if ([r, g, b].some(c => c < 0 || 255 < c)) {
            throw new RangeError('Invalid range for RGB colors');
        }
    } else if (n === 5 && numbers.length >= 1) {
        // 256 colors
        const idx = numbers.shift()!;
        if (idx < 0) {
            throw new RangeError('Color index must be >= 0');
        } else if (idx < 16) {
            // 16 default terminal colors
            return idx;
        } else if (idx < 232) {
            // 6x6x6 color cube, see https://stackoverflow.com/a/27165165/500098
            r = Math.floor((idx - 16) / 36);
            r = r > 0 ? 55 + r * 40 : 0;
            g = Math.floor(((idx - 16) % 36) / 6);
            g = g > 0 ? 55 + g * 40 : 0;
            b = (idx - 16) % 6;
            b = b > 0 ? 55 + b * 40 : 0;
        } else if (idx < 256) {
            // grayscale, see https://stackoverflow.com/a/27165165/500098
            r = g = b = (idx - 232) * 10 + 8;
        } else {
            throw new RangeError('Color index must be < 256');
        }
    } else {
        throw new RangeError('Invalid extended color specification');
    }
    return [r, g, b];
}

/**
   * Transform ANSI color escape codes into HTML <SPAN> tags with CSS
   * classes such as "ansi-green-intense-fg".
   * The actual colors used are set in the CSS file.
   * This also removes non-color escape sequences.
   * This is supposed to have the same behavior as nbconvert.filters.ansi2html()
   */
function ansiSpan(str: string): string {
    const ansiRe = /\x1b\[(.*?)([@-~])/g; // eslint-disable-line no-control-regex
    let fg: number | Array<number> = [];
    let bg: number | Array<number> = [];
    let bold = false;
    let underline = false;
    let inverse = false;
    let match;
    const out: Array<string> = [];
    const numbers = [];
    let start = 0;

    str = escape(str);

    str += '\x1b[m'; // Ensure markup for trailing text
    // tslint:disable-next-line
    while ((match = ansiRe.exec(str))) {
        if (match[2] === 'm') {
            const items = match[1].split(';');
            for (let i = 0; i < items.length; i++) {
                const item = items[i];
                if (item === '') {
                    numbers.push(0);
                } else if (item.search(/^\d+$/) !== -1) {
                    numbers.push(parseInt(item, 10));
                } else {
                    // Ignored: Invalid color specification
                    numbers.length = 0;
                    break;
                }
            }
        } else {
            // Ignored: Not a color code
        }
        const chunk = str.substring(start, match.index);
        pushColoredChunk(chunk, fg, bg, bold, underline, inverse, out);
        start = ansiRe.lastIndex;

        while (numbers.length) {
            const n = numbers.shift();
            switch (n) {
                case 0:
                    fg = bg = [];
                    bold = false;
                    underline = false;
                    inverse = false;
                    break;
                case 1:
                case 5:
                    bold = true;
                    break;
                case 4:
                    underline = true;
                    break;
                case 7:
                    inverse = true;
                    break;
                case 21:
                case 22:
                    bold = false;
                    break;
                case 24:
                    underline = false;
                    break;
                case 27:
                    inverse = false;
                    break;
                case 30:
                case 31:
                case 32:
                case 33:
                case 34:
                case 35:
                case 36:
                case 37:
                    fg = n - 30;
                    break;
                case 38:
                    try {
                        fg = getExtendedColors(numbers);
                    } catch (e) {
                        numbers.length = 0;
                    }
                    break;
                case 39:
                    fg = [];
                    break;
                case 40:
                case 41:
                case 42:
                case 43:
                case 44:
                case 45:
                case 46:
                case 47:
                    bg = n - 40;
                    break;
                case 48:
                    try {
                        bg = getExtendedColors(numbers);
                    } catch (e) {
                        numbers.length = 0;
                    }
                    break;
                case 49:
                    bg = [];
                    break;
                case 90:
                case 91:
                case 92:
                case 93:
                case 94:
                case 95:
                case 96:
                case 97:
                    fg = n - 90 + 8;
                    break;
                case 100:
                case 101:
                case 102:
                case 103:
                case 104:
                case 105:
                case 106:
                case 107:
                    bg = n - 100 + 8;
                    break;
                default:
                // Unknown codes are ignored
            }
        }
    }
    return out.join('');
}
