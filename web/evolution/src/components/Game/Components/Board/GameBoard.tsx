import { useContext, useEffect, useState } from "react";
import GameContext from "@/context/GameContext";
import { Box, Typography, IconButton, Card, CardContent, CardActions, Dialog, DialogTitle, DialogContent, Chip } from "@mui/material";
import StartGameButton from "@/components/Game/Components/Buttons/StartGameButton";
import { callApi } from "@/utils/callApi";
import { Game } from "@/types/types";
import { SwapVert, Flip, PlayArrow } from "@mui/icons-material";

type Phase = "Phase.DEVELOPMENT" | "Phase.AREAS" | "Phase.FEEDING" | "Phase.EXTINCTION";

interface Trait {
  name: string;
  description: string;
  trait_classes: string[];
  food_requirement: number;
}

interface CardData {
  traits: Trait[];
}

interface CardTrayProps {
  hand: CardData[];
  flippedCards: {[key: number]: boolean};
  cardTraits: {[key: number]: Trait[]};
  onTraitClick: (trait: Trait) => void;
  onFlipCard: (index: number) => void;
  onSwapTraits: (cardIndex: number) => void;
  onPlayCard: (cardIndex: number) => void;
  currentPhase?: Phase;
}

function CardTray({ hand, flippedCards, cardTraits, onTraitClick, onFlipCard, onSwapTraits, onPlayCard, currentPhase }: CardTrayProps) {
  return (
    <Box sx={{ 
      position: 'fixed', 
      bottom: 0, 
      left: 0, 
      right: 0, 
      p: 2, 
      display: 'flex', 
      justifyContent: 'center',
      gap: 2, 
      bgcolor: 'background.paper',
      overflowX: 'auto'
    }}>
      {hand.slice(0, 6).map((card, cardIndex) => (
        <Card key={cardIndex} sx={{ 
          minWidth: 170,
          maxWidth: 170,
          height: 120,
          display: 'flex',
          flexDirection: 'column'
        }}>
          <CardContent sx={{ 
            flexGrow: 1,
            p: 1,
            pb: 0
          }}>
            {flippedCards[cardIndex] ? (
              <Typography variant="h6">New Animal</Typography>
            ) : (
              <Box>
                {cardTraits[cardIndex]?.map((trait, traitIndex) => (
                  <Box
                    key={traitIndex}
                    sx={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      cursor: 'pointer',
                      '&:hover': { bgcolor: 'action.hover' }
                    }}
                    onClick={() => onTraitClick(trait)}
                  >
                    <Typography variant="body1">{trait.name}</Typography>
                    {trait.food_requirement > 0 && (
                      <Typography variant="body2">+{trait.food_requirement}</Typography>
                    )}
                  </Box>
                ))}
              </Box>
            )}
          </CardContent>
          <CardActions sx={{ justifyContent: 'center', p: 0.5 }}>
            {!flippedCards[cardIndex] && (
              <IconButton size="small" onClick={() => onSwapTraits(cardIndex)}>
                <SwapVert fontSize="small" />
              </IconButton>
            )}
            <IconButton size="small" onClick={() => onFlipCard(cardIndex)}>
              <Flip fontSize="small" />
            </IconButton>
            {currentPhase === "Phase.DEVELOPMENT" && (
              <IconButton size="small" onClick={() => onPlayCard(cardIndex)}>
                <PlayArrow fontSize="small" />
              </IconButton>
            )}
          </CardActions>
        </Card>
      ))}
    </Box>
  );
}

export default function GameBoard() {
  const { game, setGame } = useContext(GameContext);
  const [isPolling, setIsPolling] = useState(false);
  const [selectedTrait, setSelectedTrait] = useState<Trait | null>(null);
  const [flippedCards, setFlippedCards] = useState<{[key: number]: boolean}>({});
  const [cardTraits, setCardTraits] = useState<{[key: number]: Trait[]}>({});
  const [swappedCards, setSwappedCards] = useState<{[key: number]: boolean}>({});

  // Reset all state when game ID changes
  useEffect(() => {
    if (game?.id) {
      setIsPolling(false);
      setSelectedTrait(null);
      setFlippedCards({});
      setCardTraits({});
      setSwappedCards({});
    }
  }, [game?.id]);

  useEffect(() => {
    let intervalId: NodeJS.Timeout;

    const pollGame = async () => {
      if (!game?.id) return;

      try {
        const result = await callApi<Game>("get", `api/game/${game.id}/`);
        if (result.success && result.data) {
          setGame(result.data);
          
          // Start polling if game starts
          if (result.data.started && !isPolling) {
            setIsPolling(true);
          }
        }
      } catch (error) {
        console.error("Error polling game:", error);
      }
    };

    if (game?.id) {
      // Initial poll
      pollGame();

      // Set up polling interval
      intervalId = setInterval(pollGame, 3000);
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [game?.id, setGame, isPolling]);

  useEffect(() => {
    if (!game?.this_player?.hand) return;

    setCardTraits(prev => {
      const newTraits: {[key: number]: Trait[]} = {};
      game.this_player?.hand.forEach((card: CardData, index: number) => {
        if (!swappedCards[index]) {
          newTraits[index] = [...card.traits];
        } else {
          newTraits[index] = prev[index] || [...card.traits];
        }
      });
      return newTraits;
    });
  }, [game?.this_player?.hand, swappedCards]);

  if (!game) {
    return null;
  }

  const handleTraitClick = (trait: Trait) => {
    setSelectedTrait(trait);
  };

  const handleFlipCard = (index: number) => {
    setFlippedCards(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  const handleSwapTraits = (cardIndex: number) => {
    setCardTraits(prev => {
      const currentTraits = prev[cardIndex];
      if (currentTraits && currentTraits.length === 2) {
        return {
          ...prev,
          [cardIndex]: [currentTraits[1], currentTraits[0]]
        };
      }
      return prev;
    });
    setSwappedCards(prev => ({
      ...prev,
      [cardIndex]: true
    }));
  };

  const handlePlayCard = (cardIndex: number) => {
    // Implementation for playing card
  };

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" gutterBottom>
        Game Details
      </Typography>

      <Typography variant="body1">Game ID: {game.id}</Typography>

      <Typography variant="body1">
        Created At: {new Date(game.created_at).toLocaleString()}
      </Typography>

      <Typography variant="body1">
        Status:{" "}
        {game.started ? (game.ended ? "Ended" : "In Progress") : "Not Started"}
      </Typography>

      <Typography variant="body1">
        Current Epoch: {game.current_epoch?.epoch_number || "N/A"}
        <br />
        Current Phase: {game.current_epoch?.current_phase || "N/A"}
      </Typography>

      {!game.started && game.created_by_this_user && (
        <Box sx={{ mt: 2 }}>
          <StartGameButton gameId={game.id} onGameStarted={() => setIsPolling(true)} />
        </Box>
      )}

      <Typography variant="h5" sx={{ mt: 2, mb: 1 }}>
        Players ({game.player_count})
      </Typography>

      {game.this_player && (
        <Box sx={{ mb: 2 }}>
          <Typography variant="h6">Your Player</Typography>
          <Typography variant="body1">
            Score: {game.this_player.score}
          </Typography>
          <Typography variant="body1">
            Animals: {game.this_player.animals.length}
          </Typography>
        </Box>
      )}

      {game.other_players.map((player, index) => (
        <Box key={index} sx={{ mb: 2 }}>
          <Typography variant="h6">Player {player.email}</Typography>
          <Typography variant="body1">Score: {player.score}</Typography>
          <Typography variant="body1">
            Animals: {player.animals.length}
          </Typography>
          <Typography variant="body1">
            Cards in Hand: {player.hand_count}
          </Typography>
        </Box>
      ))}

      {game.this_player?.hand && (
        <CardTray
          hand={game.this_player.hand}
          flippedCards={flippedCards}
          cardTraits={cardTraits}
          onTraitClick={handleTraitClick}
          onFlipCard={handleFlipCard}
          onSwapTraits={handleSwapTraits}
          onPlayCard={handlePlayCard}
          currentPhase={game.current_epoch?.current_phase as Phase}
        />
      )}

      {/* Trait Detail Modal */}
      <Dialog open={!!selectedTrait} onClose={() => setSelectedTrait(null)}>
        <DialogTitle>{selectedTrait?.name}</DialogTitle>
        <DialogContent>
          <Typography>{selectedTrait?.description?.replace(/Icons\.animal/g, '🦒').replace(/Icons\.meat/g, '🥩').replace(/Icons\.food/g, '🫐').replace(/Icons\.fat/g, '🥓')}</Typography>
          <Typography sx={{ mt: 1 }}>
            Food Requirement: {selectedTrait?.food_requirement && selectedTrait.food_requirement > 0 ? '+' : ''}{selectedTrait?.food_requirement || 0}
          </Typography>
          <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {selectedTrait?.trait_classes.map((traitClass, index) => (
              <Chip key={index} label={traitClass} size="small" />
            ))}
          </Box>
        </DialogContent>
      </Dialog>
    </Box>
  );
}
