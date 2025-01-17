export interface Player {
  email: string;
  score: number;
  animals: any[]; // TODO: Define Animal type
  animal_order: any[];
}

export interface PlayerDetail extends Player {
  id: string;
  hand: any[];
}

export interface Game {
  id: string;
  created_at: string;
  created_by_this_user: boolean;
  player_table: any[];
  active_areas: any[];
  started: boolean;
  ended: boolean;
  current_epoch: number;
  this_player: PlayerDetail | null;
  other_players: Player[];
  player_count: number;
}
