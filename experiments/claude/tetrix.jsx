import React, { useState, useEffect, useCallback } from 'react';

const BOARD_WIDTH = 10;
const BOARD_HEIGHT = 20;
const INITIAL_DROP_TIME = 1000;

// Tetromino shapes and their rotations
const TETROMINOES = {
  I: {
    shape: [
      [0, 0, 0, 0],
      [1, 1, 1, 1],
      [0, 0, 0, 0],
      [0, 0, 0, 0]
    ],
    color: 'bg-cyan-500'
  },
  J: {
    shape: [
      [1, 0, 0],
      [1, 1, 1],
      [0, 0, 0]
    ],
    color: 'bg-blue-500'
  },
  L: {
    shape: [
      [0, 0, 1],
      [1, 1, 1],
      [0, 0, 0]
    ],
    color: 'bg-orange-500'
  },
  O: {
    shape: [
      [1, 1],
      [1, 1]
    ],
    color: 'bg-yellow-500'
  },
  S: {
    shape: [
      [0, 1, 1],
      [1, 1, 0],
      [0, 0, 0]
    ],
    color: 'bg-green-500'
  },
  T: {
    shape: [
      [0, 1, 0],
      [1, 1, 1],
      [0, 0, 0]
    ],
    color: 'bg-purple-500'
  },
  Z: {
    shape: [
      [1, 1, 0],
      [0, 1, 1],
      [0, 0, 0]
    ],
    color: 'bg-red-500'
  }
};

const createEmptyBoard = () => 
  Array.from({ length: BOARD_HEIGHT }, () => 
    Array.from({ length: BOARD_WIDTH }, () => null)
  );

const TetrisGame = () => {
  const [board, setBoard] = useState(createEmptyBoard());
  const [currentPiece, setCurrentPiece] = useState(null);
  const [currentPosition, setCurrentPosition] = useState({ x: 0, y: 0 });
  const [gameOver, setGameOver] = useState(false);
  const [score, setScore] = useState(0);
  const [level, setLevel] = useState(1);
  const [dropTime, setDropTime] = useState(INITIAL_DROP_TIME);

  const getRandomTetromino = () => {
    const pieces = Object.keys(TETROMINOES);
    const randPiece = pieces[Math.floor(Math.random() * pieces.length)];
    return {
      shape: TETROMINOES[randPiece].shape,
      color: TETROMINOES[randPiece].color
    };
  };

  const isColliding = useCallback((piece, position) => {
    for (let y = 0; y < piece.shape.length; y++) {
      for (let x = 0; x < piece.shape[y].length; x++) {
        if (piece.shape[y][x]) {
          const newX = position.x + x;
          const newY = position.y + y;
          
          if (
            newX < 0 || 
            newX >= BOARD_WIDTH ||
            newY >= BOARD_HEIGHT ||
            (newY >= 0 && board[newY][newX])
          ) {
            return true;
          }
        }
      }
    }
    return false;
  }, [board]);

  const rotatePiece = useCallback((piece) => {
    const newShape = piece.shape[0].map((_, i) =>
      piece.shape.map(row => row[i]).reverse()
    );
    return { ...piece, shape: newShape };
  }, []);

  const tryRotate = useCallback(() => {
    if (!currentPiece) return;
    
    const rotatedPiece = rotatePiece(currentPiece);
    if (!isColliding(rotatedPiece, currentPosition)) {
      setCurrentPiece(rotatedPiece);
    }
  }, [currentPiece, currentPosition, rotatePiece, isColliding]);

  const moveHorizontally = useCallback((delta) => {
    if (!currentPiece) return;
    
    const newPosition = { ...currentPosition, x: currentPosition.x + delta };
    if (!isColliding(currentPiece, newPosition)) {
      setCurrentPosition(newPosition);
    }
  }, [currentPiece, currentPosition, isColliding]);

  const clearLines = useCallback(() => {
    let linesCleared = 0;
    const newBoard = board.reduce((acc, row) => {
      if (row.every(cell => cell !== null)) {
        linesCleared++;
        acc.unshift(Array(BOARD_WIDTH).fill(null));
      } else {
        acc.push(row);
      }
      return acc;
    }, []);

    if (linesCleared > 0) {
      setBoard(newBoard);
      setScore(prev => prev + (linesCleared * 100 * level));
      setLevel(prev => Math.floor(score / 1000) + 1);
      setDropTime(INITIAL_DROP_TIME * Math.pow(0.9, level - 1));
    }
  }, [board, level, score]);

  const mergePiece = useCallback(() => {
    if (!currentPiece) return;

    const newBoard = [...board];
    currentPiece.shape.forEach((row, y) => {
      row.forEach((value, x) => {
        if (value) {
          const newY = currentPosition.y + y;
          if (newY >= 0) {
            newBoard[newY][currentPosition.x + x] = currentPiece.color;
          }
        }
      });
    });

    setBoard(newBoard);
    clearLines();
    
    const newPiece = getRandomTetromino();
    const newPosition = { x: Math.floor(BOARD_WIDTH / 2) - 2, y: -2 };
    
    if (isColliding(newPiece, newPosition)) {
      setGameOver(true);
    } else {
      setCurrentPiece(newPiece);
      setCurrentPosition(newPosition);
    }
  }, [board, currentPiece, currentPosition, clearLines, isColliding]);

  const moveDown = useCallback(() => {
    if (!currentPiece) return;
    
    const newPosition = { ...currentPosition, y: currentPosition.y + 1 };
    if (!isColliding(currentPiece, newPosition)) {
      setCurrentPosition(newPosition);
    } else {
      mergePiece();
    }
  }, [currentPiece, currentPosition, isColliding, mergePiece]);

  // Initialize game
  useEffect(() => {
    if (!currentPiece) {
      const newPiece = getRandomTetromino();
      setCurrentPiece(newPiece);
      setCurrentPosition({ x: Math.floor(BOARD_WIDTH / 2) - 2, y: -2 });
    }
  }, [currentPiece]);

  // Handle keyboard controls
  useEffect(() => {
    const handleKeyPress = (event) => {
      if (gameOver) return;
      
      switch (event.key) {
        case 'ArrowLeft':
          moveHorizontally(-1);
          break;
        case 'ArrowRight':
          moveHorizontally(1);
          break;
        case 'ArrowDown':
          moveDown();
          break;
        case 'ArrowUp':
          tryRotate();
          break;
        case ' ':
          // Hard drop
          while (!isColliding(currentPiece, { ...currentPosition, y: currentPosition.y + 1 })) {
            setCurrentPosition(prev => ({ ...prev, y: prev.y + 1 }));
          }
          mergePiece();
          break;
        default:
          break;
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [currentPiece, currentPosition, gameOver, moveHorizontally, moveDown, tryRotate, isColliding, mergePiece]);

  // Handle automatic dropping
  useEffect(() => {
    if (gameOver) return;
    
    const dropInterval = setInterval(moveDown, dropTime);
    return () => clearInterval(dropInterval);
  }, [moveDown, dropTime, gameOver]);

  // Render game board with current piece
  const renderBoard = () => {
    const displayBoard = board.map(row => [...row]);
    
    if (currentPiece) {
      currentPiece.shape.forEach((row, y) => {
        row.forEach((value, x) => {
          if (value) {
            const boardY = currentPosition.y + y;
            const boardX = currentPosition.x + x;
            if (boardY >= 0 && boardY < BOARD_HEIGHT && boardX >= 0 && boardX < BOARD_WIDTH) {
              displayBoard[boardY][boardX] = currentPiece.color;
            }
          }
        });
      });
    }

    return displayBoard;
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 p-4">
      <div className="mb-4 text-white">
        <div className="text-2xl font-bold mb-2">Score: {score}</div>
        <div className="text-xl">Level: {level}</div>
      </div>
      
      <div className="border-4 border-gray-700 bg-gray-800 p-1">
        {renderBoard().map((row, y) => (
          <div key={y} className="flex">
            {row.map((cell, x) => (
              <div
                key={`${x}-${y}`}
                className={`w-6 h-6 border border-gray-700 ${cell || 'bg-gray-900'}`}
              />
            ))}
          </div>
        ))}
      </div>
      
      {gameOver && (
        <div className="mt-4 text-white text-2xl font-bold">
          Game Over! Score: {score}
        </div>
      )}
      
      <div className="mt-4 text-white text-sm">
        <p>Controls:</p>
        <p>← → : Move left/right</p>
        <p>↑ : Rotate</p>
        <p>↓ : Move down</p>
        <p>Space : Hard drop</p>
      </div>
    </div>
  );
};

export default TetrisGame;
