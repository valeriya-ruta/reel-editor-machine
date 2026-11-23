// Palette and type for the explainer world. Two families: crisp UI (Claude's
// cream and terracotta) and shaded "physical" metaphor objects.

import {staticFile} from 'remotion';

export const C = {
  ink: '#1F1F22',
  marker: '#FDE293',
  // Claude UI
  cream: '#FAF9F5',
  terracotta: '#D97757',
  claudeText: '#2B2925',
  claudeLine: '#E3DED5',
  claudeHair: '#ECE7DF',
  claudeMuted: '#A8A29A',
  bubble: '#EFE9DF',
  // physical objects
  paper: ['#FFD6E2', '#FBC4D4', '#F6B0C5'],
  paperBack: ['#F3A3BB', '#E98AA6'],
  paperText: '#4A2734',
  folder: ['#F6B511', '#DD9500'],
  folderFront: ['#FFDB6E', '#F7BF22'],
  skill: ['#FFE0E9', '#F6A9C0'],
  deviceDark: 'linear-gradient(160deg,#3D3E44 0,#1B1C1F 60%,#25262A 100%)',
  alu: 'linear-gradient(#F2F3F5 0,#D4D7DC 35%,#AEB2B9 100%)',
};

export const FONT = "'Onest', system-ui, sans-serif";
export const SERIF = "'Lora', Georgia, serif";

export const asset = (p: string) => staticFile(p);

/** Soft contact shadow under anything that rests on the desk. */
export const contactShadow = (opacity = 0.28) =>
  `radial-gradient(closest-side, rgba(20,22,30,${opacity}), rgba(20,22,30,0))`;
