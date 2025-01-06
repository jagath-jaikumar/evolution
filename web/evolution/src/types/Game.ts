export interface Game {
  id: string;
  players: string[];
  epoch: number;
  ended?: boolean;
  started?: boolean;
}
