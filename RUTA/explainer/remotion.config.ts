import {Config} from '@remotion/cli/config';

// H.264, never HEVC: Instagram and every phone play it, and it is what she posts.
Config.setCodec('h264');
Config.setCrf(18);
Config.setPixelFormat('yuv420p');
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
