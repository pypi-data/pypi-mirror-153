/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global, LI, SPAN } from '../../../Global';

import DirListingItemIcon from './DirListingItemIcon'
import { FilterableFile } from './DirListingContent';

import moment from 'moment'
import { StringExt } from '@lumino/algorithm';
import FormatUtils from '../../../utils/FormatUtils';
import { FileMetadata } from './FileBrowser';
import { VersionHistory } from '../../settings/VersionHistory';
import IconButton from '@mui/material/IconButton';
import { Delete, GetApp } from '@mui/icons-material';

interface IProps {
    file: FilterableFile
    filter: string
    selected: boolean
    showReferences: boolean
    showVersionHistory: boolean
    onClick: (event: React.MouseEvent<HTMLLIElement, MouseEvent>) => void
    onDoubleClick: (event: React.MouseEvent<HTMLLIElement, MouseEvent>) => void
    onDownload?: (file: FileMetadata) => void
    onDelete?: (file: FileMetadata) => void
}

interface IState {
    hovered: boolean
}

const fileTitle = (file: FileMetadata) => (
    'Name: ' + file.name + '\n' +
    (file.size === null ? '' : 'Size: ' + FormatUtils.styleCapacityUnitValue()(file.size) + (Global.isDevVersion ? ' (' + file.size + ' bytes)' : '') + '\n') +
    (file.path === '' ? '' : 'Path: ' + file.path.replace(file.name, '').replace(/\/$/, '') + '\n') + 
    'Modified: ' + moment(file.last_modified).format('YYYY-MM-DD hh:mm:ss')
)

export default class DirListingItem extends React.Component<IProps, IState> {

    constructor(props: IProps) {
        super(props)
        this.state = {
            hovered: false
        }
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const file = this.props.file.file
        var html = StringExt.highlight(file.name, this.props.file.indices, (s: string) => '<mark style="padding: 0px;">' + s + '</mark>').join('');
        if (this.props.showReferences && file.type != 'directory' && file.content?.length > 1) html += '<SPAN style="margin-left: 6px; opacity: 0.5;">is referenced by ' + file.content.length + ' workloads</SPAN>'
        const hidableIcon = (this.props.onDownload != undefined) || (this.props.onDelete != undefined)
        return (
            <DIV sx={{position: 'relative'}}>
                <LI
                    onMouseOver={() => this.setState({hovered: true})}
                    onMouseOut={() => this.setState({hovered: false})}
                    className={'jp-DirListing-item' + (this.props.selected ? ' jp-mod-selected' : '')}
                    onClick={(event: React.MouseEvent<HTMLLIElement, MouseEvent>) => this.props.onClick(event)}
                    onDoubleClick={(event: React.MouseEvent<HTMLLIElement, MouseEvent>) => this.props.onDoubleClick(event)}
                    title={fileTitle(file)}
                    style={{padding: hidableIcon ? '8px 12px' : '4px 12px', background : !this.props.selected && this.state.hovered ? 'var(--jp-layout-color2)' : ''}}
                >
                    <DirListingItemIcon fileType={file.type} mimetype={file.mimetype} />
                    <SPAN className='jp-DirListing-itemText' dangerouslySetInnerHTML={{ __html: html }}/>
                    <SPAN
                        sx={{ opacity: this.state.hovered && hidableIcon ? 0 : 1, }}
                        className='jp-DirListing-itemModified'
                        title={moment(file.last_modified).format('MMM D, YYYY h:mm A')}
                    >
                        {moment(file.last_modified).fromNow()}
                    </SPAN>
                </LI>
                {hidableIcon && (
                    <DIV 
                        sx={{
                            display: 'inline-flex', 
                            position: 'absolute', 
                            right: '0px', 
                            top: '0px',
                            opacity: this.state.hovered ? 1 : 0, 
                            transition: 'opacity 300ms ease-in-out'
                        }}
                        onMouseOver={() => this.setState({hovered: true})}
                        onMouseOut={() => this.setState({hovered: false})}
                    >
                        {this.props.showVersionHistory && file.type != 'directory' && file.content.length > 1 &&  (
                            <VersionHistory 
                                onClose={() => this.setState({ hovered: false })} 
                                metadata={file} 
                                onDownload={this.props.onDownload} 
                                onDelete={this.props.onDelete}
                            />
                        )}
                        {this.props.onDownload && (
                            <IconButton
                                size='large'
                                onClick={() => this.props.onDownload(file)}
                                sx={{ width: '36px', height: '36px', padding: '4px 3px 2px 3px' }}
                            >
                                <GetApp sx={{ width: '30px', height: '30px', padding: '3px' }} />
                            </IconButton>
                        )}
                        {this.props.onDelete && (
                            <IconButton
                                size='large'
                                onClick={() => this.props.onDelete(file)}
                                sx={{ width: '36px', height: '36px', padding: '3px' }}
                            >
                                <Delete sx={{ width: '30px', height: '30px', padding: '3px' }} />
                            </IconButton>
                        )}
                    </DIV>
                )}
            </DIV>
        )
    }
}
