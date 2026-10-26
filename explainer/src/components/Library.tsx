// A contact sheet of the object library in representative states — the
// "library" composition in Studio. Used to check the look of every object
// without scrubbing through an episode.

import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import type {SceneObject} from '../engine/types';
import {initialState, localBounds} from '../engine/world';
import type {State, World} from '../objects/core';
import {OBJECTS} from '../objects/registry';
import {useFonts} from './fonts';

type Item = {o: SceneObject; s?: Partial<State>};

const ITEMS: Item[] = [
  {o: {id: 'laptop', type: 'laptop', x: 300, y: 380, scale: 0.6}, s: {typed: 'Зроби контент-план на тиждень', sel: false}},
  {o: {id: 'call', type: 'laptop', x: 790, y: 380, scale: 0.5, props: {window: 'call'}}, s: {rec: 1, speaking: 'client'}},
  {o: {id: 'player', type: 'laptop', x: 790, y: 640, scale: 0.5, props: {window: 'player'}}, s: {scrubP: 0.06}},
  {o: {id: 'phone', type: 'phone', x: 140, y: 690, scale: 1.1}, s: {chatP: 1, chatUser: '/дзвінок', replyP: 1, replyTitle: 'Готово'}},
  {o: {id: 'ruta', type: 'chibi', x: 380, y: 860, scale: 0.6, props: {pose: 'furious'}}},
  {o: {id: 'paper', type: 'paper', x: 200, y: 900, scale: 0.7, props: {text: 'Зроби контент-план на тиждень у моєму стилі'}}},
  {o: {id: 'folder', type: 'folder', x: 160, y: 1240, scale: 0.6, props: {label: 'промпти', full: true}}},
  {o: {id: 'skill', type: 'skill', x: 760, y: 760, scale: 0.75, props: {name: '/дзвінок'}}, s: {stampP: 1}},
  {o: {id: 'notepad', type: 'notepad', x: 400, y: 1150, scale: 0.55}, s: {ink: 0.6}},
  {o: {id: 'chips', type: 'chips', x: 800, y: 980, scale: 0.6, props: {items: ['дедлайн — п’ятниця', '3 рілси', 'бриф', 'ціна?']}}, s: {pop: 1}},
  {o: {id: 'fathom', type: 'app', x: 640, y: 1290, scale: 0.5, props: {app: 'fathom', label: 'Fathom'}}},
  {o: {id: 'claude', type: 'app', x: 940, y: 1290, scale: 0.5, props: {app: 'claude', label: 'Claude'}}},
  {o: {id: 'cable', type: 'cable', x: 0, y: 0, props: {from: 'fathom', to: 'claude'}}, s: {plugP: 1}},
  {
    o: {
      id: 'tasks',
      type: 'tasks',
      x: 780,
      y: 1620,
      scale: 0.6,
      props: {title: 'ClickUp · Олена', logo: 'clickup', items: [{text: 'Бриф для Олени', due: 'пт'}, {text: '3 сценарії рілсів', due: '04.11'}, {text: 'Оффер: пакет «Старт»', due: 'сьогодні'}]},
    },
    s: {shown: 3, checks: {0: 1}},
  },
  {o: {id: 'offer', type: 'paper', x: 280, y: 1600, scale: 0.55, props: {title: 'Оффер', sub: 'чернетка', bars: 6, w: 420, h: 520}}},
];

export const Library: React.FC = () => {
  useFonts();
  const t = useCurrentFrame() / 30;
  const states: Record<string, State> = {};
  const objects: Record<string, SceneObject> = {};
  for (const {o, s} of ITEMS) {
    objects[o.id] = o;
    states[o.id] = {...initialState(o), ...(s ?? {})};
  }
  const world: World = {t, states, objects, boundsOf: (id, anchor) => (objects[id] ? localBounds(objects[id], states[id], anchor) : null)};
  return (
    <AbsoluteFill style={{background: 'radial-gradient(120% 70% at 50% 35%,#FFFFFF 0,#F7F8FA 70%,#EEF0F4 100%)'}}>
      {ITEMS.map(({o}) => {
        const def = OBJECTS[o.type];
        const R = def.Render;
        if (def.raw) return <R key={o.id} o={o} s={states[o.id]} t={t} world={world} />;
        const size = def.size(o);
        const ax = size.ax ?? 0.5;
        const ay = size.ay ?? 1;
        return (
          <div key={o.id} style={{position: 'absolute', left: o.x - ax * size.w, top: o.y - ay * size.h, width: size.w, height: size.h, transformOrigin: `${ax * 100}% ${ay * 100}%`, transform: `scale(${o.scale ?? 1})`}}>
            <R o={o} s={states[o.id]} t={t} world={world} />
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
