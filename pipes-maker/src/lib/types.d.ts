export interface Board {
  pipes: Pipe[];
  height: number;
  width: number;
}

export interface Pipe {
  joints: [boolean, boolean, boolean, boolean];
}
