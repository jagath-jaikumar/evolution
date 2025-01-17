export interface Player {
  email: string;
  score: number;
  animals: any[];
  animal_order: any[];
  hand_count: number;
}

export interface PlayerDetail extends Player {
  id: string;
  hand: any[];
}

export interface Epoch {
  id: string;
  epoch_number: number;
  current_phase: string;
}

export interface Game {
  id: string;
  created_at: string;
  created_by_this_user: boolean;
  player_table: any[];
  active_areas: any[];
  started: boolean;
  ended: boolean;
  current_epoch: Epoch | null;
  this_player: PlayerDetail | null;
  other_players: Player[];
  player_count: number;
}
