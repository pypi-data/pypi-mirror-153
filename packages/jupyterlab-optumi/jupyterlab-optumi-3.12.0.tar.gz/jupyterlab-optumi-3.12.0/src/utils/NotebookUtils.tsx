/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

export default class NotebookUtils {
    // Remove chunks that should be overridden by the effect of
    // carriage return characters
    public static fixCarriageReturn(txt: string) {
        txt = txt.replace(/\r+\n/gm, '\n'); // \r followed by \n --> newline
        while (txt.search(/\r[^$]/g) > -1) {
            var base = txt.match(/^(.*)\r+/m)[1];
            var insert = txt.match(/\r+(.*)$/m)[1];
            insert = insert + base.slice(insert.length, base.length);
            txt = txt.replace(/\r+.*$/m, '\r').replace(/^.*\r/m, insert);
        }
        return txt;
    }

    // Remove characters that are overridden by backspace characters
    public static fixBackspace(txt: string) {
        var tmp = txt;
        do {
            txt = tmp;
            // Cancel out anything-but-newline followed by backspace
            tmp = txt.replace(/\n?[^\x08]\x08/g, '');
        } while (tmp.length < txt.length);
        return txt;
    }

    // Remove characters overridden by backspace and carriage return
    public static fixOverwrittenChars(txt: string | string[]) {
        if (Array.isArray(txt)) {
            return NotebookUtils.fixBackspace(NotebookUtils.fixCarriageReturn(txt.join('')));

        } else {
            return NotebookUtils.fixBackspace(NotebookUtils.fixCarriageReturn(txt));
        }
    }
}