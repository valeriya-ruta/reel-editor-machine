// Every object type an episode spec may place in its scene. Adding a type here
// (and nothing else) makes it usable from any episode.

import {AppTile, Cable, TaskList} from './Pipeline';
import {Chibi} from './Chibi';
import type {ObjectDef, Verb} from './core';
import {GENERIC} from './core';
import {Laptop} from './Laptop';
import {Chips, Notepad} from './Notes';
import {Folder, Paper, SkillCard} from './Paper';
import {Phone} from './Phone';

export const OBJECTS: Record<string, ObjectDef> = {
  laptop: Laptop,
  phone: Phone,
  chibi: Chibi,
  paper: Paper,
  folder: Folder,
  skill: SkillCard,
  notepad: Notepad,
  chips: Chips,
  app: AppTile,
  cable: Cable,
  tasks: TaskList,
};

export const verbFor = (type: string, verb: string): Verb | undefined => OBJECTS[type]?.verbs[verb] ?? GENERIC[verb];

export const verbsOf = (type: string) => [...Object.keys(OBJECTS[type]?.verbs ?? {}), ...Object.keys(GENERIC)];
