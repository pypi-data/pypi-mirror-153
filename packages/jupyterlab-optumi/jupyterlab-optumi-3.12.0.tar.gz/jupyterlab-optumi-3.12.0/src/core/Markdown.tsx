/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../Global';

import { SxProps, Theme } from '@mui/system';

import * as rendermime from '@jupyterlab/rendermime';
import { Mode, CodeMirrorEditor } from '@jupyterlab/codemirror';
import { defaultSanitizer } from '@jupyterlab/apputils';

import marked from 'marked';

interface IProps {
    text: string
    sx?: SxProps<Theme>
}
interface IState {}

export class Markdown extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
        // Separate math from normal markdown text.
        const parts = rendermime.removeMath(this.props.text);
        // Convert the markdown to HTML.
        let html = renderMarked(parts['text']);
        // Replace math.
        html = rendermime.replaceMath(html, parts['math']);
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV sx={Object.assign({}, this.props.sx)} dangerouslySetInnerHTML={{ __html: defaultSanitizer.sanitize(html) }} />
        )
    }
}

/// The functions below were taken from https://github.com/jupyterlab/jupyterlab/blob/b05c2748c021a8da681315fd0a6bcaee01e96d6b/packages/rendermime/src/renderers.ts

let markedInitialized = false;

  /**
   * Support GitHub flavored Markdown, leave sanitizing to external library.
   */
function initializeMarked(): void {
    if (markedInitialized) {
        return;
    }
    markedInitialized = true;
    marked.setOptions({
        gfm: true,
        sanitize: false,
        // breaks: true; We can't use GFM breaks as it causes problems with tables
        langPrefix: `cm-s-${CodeMirrorEditor.defaultConfig.theme} language-`,
        highlight: (code, lang, callback) => {
        const cb = (err: Error | null, code: string) => {
            if (callback) {
            callback(err, code);
            }
            return code;
        };
        if (!lang) {
            // no language, no highlight
            return cb(null, code);
        }
        Mode.ensure(lang)
            .then(spec => {
            const el = document.createElement('div');
            if (!spec) {
                console.error(`No CodeMirror mode: ${lang}`);
                return cb(null, code);
            }
            try {
                Mode.run(code, spec.mime, el);
                return cb(null, el.innerHTML);
            } catch (err: any) {
                console.error(`Failed to highlight ${lang} code`, err);
                return cb(err, code);
            }
            })
            .catch(err => {
            console.error(`No CodeMirror mode: ${lang}`);
            console.error(`Require CodeMirror mode error: ${err}`);
            return cb(null, code);
            });
        return code;
        }
    });
}


/**
   * Render markdown for the specified content.
   *
   * @param content - The string of markdown to render.
   *
   * @return A promise which resolves with the rendered content.
   */
function renderMarked(content: string): string {
    initializeMarked();
    return marked(content)
  }
