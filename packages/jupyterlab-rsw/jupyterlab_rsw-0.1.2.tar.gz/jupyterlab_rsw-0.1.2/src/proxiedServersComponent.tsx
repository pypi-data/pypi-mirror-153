/*
 * proxiedServersComponent.tsx
 *
 * Copyright (C) 2022 by RStudio, PBC
 *
 */

// This file shares variables with './jupyterlab_rsw/constants.py'
import React, { Component, Fragment } from 'react';
import { launcherIcon } from '@jupyterlab/ui-components';

const TitleComponent = (props: { title: string }): JSX.Element => {
  const headerId = ('title_component_' + props.title).replace(/\s+/g, '_');
  return (
    <div>
      <header id={headerId}>{props.title}</header>
    </div>
  );
};

const ServerComponent = (props: { server: Server }): JSX.Element => {
  const hyperlinkId = 'server_link_' + props.server.html_id;
  const liId = 'server_component_' + props.server.html_id;
  const serverNameId = 'server_name_' + props.server.html_id;
  const serverInfoId = 'server_info_' + props.server.html_id;
  return ( 
    <Fragment aria-role='link' aria-label={'Open link for proxied server ' + props.server.label}>
      <a id={hyperlinkId} target="_blank" title={props.server.title} href={props.server.securePath}>
        <li id={liId}>
          <launcherIcon.react paddingRight={5}/>
          <span id={serverNameId} className='jp-ServerName'>{props.server.label}</span>
          <span id={serverInfoId} className='jp-ServerInfo'>{props.server.ip}:{props.server.port}</span>
        </li>
      </a>
    </Fragment>
  );
}

export interface Props {
  servers: Array<Server>;
}

export interface State {}

export class ProxiedServersComponent extends Component<Props, State> {
  constructor(props: { servers: Array<Server> }) {
    super(props);
  }

  render() {
    const serverItems = this.props.servers.map((server) =>
      <ServerComponent server={server} />
    );
  
    return(
      <Fragment>
        <TitleComponent title='Proxied Servers'/>
        <div>
          <ul id='proxied_servers_list'>
            {serverItems}
          </ul>
        </div>
      </Fragment>
    );
  }
}

export class Server {
  readonly pid: number;
  readonly label: string;
  readonly port: number;
  readonly securePath: string;
  readonly ip: string;
  readonly title: string;
  readonly html_id: string;

  constructor(pid: number, name: string, port: number, ip: string, securePath: string) {
    this.pid = pid;
    this.label = name;
    this.port = port;
    this.ip = ip;
    this.securePath = securePath;
    this.title = securePath && securePath != '' ? securePath : 'Could not create secure url.';

    let id_str = this.label + '_' +  port
    id_str = id_str.replace(/\s+|-/g, '_'); // replace spaces with an underscore
    this.html_id = id_str.replace(/_+/g, '_'); // remove any duplicated underscores
  }
};
