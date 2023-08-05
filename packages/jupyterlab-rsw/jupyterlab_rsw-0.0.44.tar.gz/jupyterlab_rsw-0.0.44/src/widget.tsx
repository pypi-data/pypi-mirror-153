/*
 * widget.tsx
 *
 * Copyright (C) 2022 by RStudio, PBC
 *
 */

// This file shares variables with './jupyterlab_rsw/constants.py'
import { kServerEndpoint, kUrlEndpoint } from './constants';
import { requestAPI } from './handler';
import { ProxiedServersComponent, Server } from './proxiedServersComponent';

import { ReactWidget, UseSignal } from '@jupyterlab/apputils';
import { Message } from '@lumino/messaging';
import { ISignal, Signal } from '@lumino/signaling';
import React from 'react';

function UseSignalComponent(props: { signal: ISignal<RStudioWorkbenchWidget, Server[]>, servers: Array<Server> }) {
  return <UseSignal signal={props.signal} initialArgs={props.servers}>{ (_, servers) => <ProxiedServersComponent servers={servers} />}</UseSignal>
}

export class RStudioWorkbenchWidget extends ReactWidget {
  public servers: Map<number, Server[]> = new Map<number, Server[]>();
  private _timerID: number;
  private _signal = new Signal<this, Server[]>(this);
  private _serverString: string = '';
  private _sessionUrl: string = '';

  constructor() {
    super();
    this.addClass('jp-RStudioWorkbenchWidget');
  }

  private getSessionUrl(): void {
    requestAPI<any>(kUrlEndpoint).then((response) => {
      try {
        this._sessionUrl = response.baseSessionUrl;
      } catch (error) {
        console.log(`Received invalid response on GET /jupyterlab-rsw/url. \n${error}`);
      }
    }, (error) => {
      console.log(`Error on GET /jupyterlab-rsw/url. \n${error}`);
    });
  }

  private requestServers(): void {
    requestAPI<any>(kServerEndpoint).then((response) => {
      if (JSON.stringify(response.servers) != this._serverString) {
        this._serverString = JSON.stringify(response.servers);
        this.servers.clear();
        try {
          response.servers.forEach((server) => {
            this.servers.set(server.pid, [new Server(server.pid, server.label, server.port, server.ip, `${this._sessionUrl}p/${server.secure_port}/`)]);
          });
          this._signal.emit(this.getServers());
        } catch (error) {
          console.log(`Received invalid response on GET /jupyterlab-rsw/servers. \n${response}`);
          return;
        }
      }
    }, (error)=> {
      console.log(`Error on GET /jupyterlab-rsw/servers. \n${error}`);
    });
  }

  protected async onAfterAttach(msg: Message): Promise<void> {
    super.onAfterAttach(msg);
    this.requestServers();
  }

  protected async onBeforeShow(msg: Message): Promise<void> {
    super.onBeforeShow(msg);
    this.getSessionUrl();
    this.requestServers();
    this._timerID = setInterval(() => this.requestServers(), 3000);
  }

  protected onAfterHide(msg: Message): void {
    super.onAfterHide(msg);
    clearInterval(this._timerID);
  }

  private getServers(): Array<Server> {
    let serverArray: Array<Server> = [];
    this.servers.forEach((value: Server[], key: number) => {
      serverArray = serverArray.concat(value);
    });
    return serverArray;
  }

  render(): JSX.Element {
    return (<UseSignalComponent signal={this._signal} servers={...this.getServers()} />);
  }
}
