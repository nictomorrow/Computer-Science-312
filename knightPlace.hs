import Data.List


knightPlace ::[Int] -> [[Int]]
knightPlace [] = []
knightPlace ls = knightPlace'
            where
            knightPlace' = zeroesToEmpty queenList
            queenList = conversion emptyBoardList queenTuple 
            queenTuple = safePlacements chessBoard queenWillGetYou
            queenWillGetYou = queenMoves queenIsHere chessBoardDim
            queenIsHere = queenCords ls 1
            chessBoardDim = length ls
            chessBoard = chessBoardCords chessBoardDim --This puts the nxn board into (x,y) cords for entire board
            emptyBoardList = emptyListofLists chessBoardDim [[]]







--Queen into coordinates in the form (x,y)
queenCords :: [Int] -> Int -> [(Int, Int)]
queenCords [] index = []
queenCords (x:xs) index
     | x > 0     = (index, x):queenCords xs (index + 1)
     | otherwise = queenCords xs (index + 1)

queenMoves :: [(Int, Int)] -> Int -> [(Int, Int)]
queenMoves tupleList length = combine
                      where
                      diag = map (queenDiagonal length) tupleList
                      hori = map (queenHorizontal length) tupleList
                      vert = map (queenVertical length) tupleList
                      knight = map (queenKnight length) tupleList
                      combine = combineTupleLists diag hori vert knight

queenDiagonal :: Int -> (Int, Int) -> [(Int, Int)]
queenDiagonal length (x,y) =  [ (x + a, y + b) | a <- [(-length)..length], b <- [(-length)..length], x+a > 0, x+a <= length, y+b > 0, y+b <= length, abs a == abs b]

queenHorizontal :: Int -> (Int, Int) -> [(Int, Int)]
queenHorizontal length (x,y) = [ (x + a, y) | a <- [(-length)..length], x+a > 0, x+a <= length ]

queenVertical :: Int -> (Int, Int) -> [(Int, Int)]
queenVertical length (x,y) = [ (x, y + b) | b <- [(-length)..length], y+b > 0, y+b <= length ]

queenKnight :: Int -> (Int, Int) -> [(Int, Int)]
queenKnight length (x,y) = [ (x + a, y + b) | a <- [-2, -1, 1, 2], b <- [-2, -1, 1, 2], abs a /= abs b, x+a > 0, x+a <= length, y+b > 0, y+b <= length ]

combineTupleLists :: [[(Int, Int)]] -> [[(Int, Int)]] -> [[(Int, Int)]] -> [[(Int, Int)]] -> [(Int, Int)]
combineTupleLists [] [] [] [] = []
combineTupleLists (x:diag) (y:hori) (z:vert) (k:knight) = nub ( x ++ y ++ z ++ k ++ combineTupleLists diag hori vert knight)





-- The entire board in (x,y) format
chessBoardCords :: Int -> [(Int, Int)]
chessBoardCords chessBoardDim = [ (x,y) | x <- [1..chessBoardDim], y <- [1..chessBoardDim] ]


--Taking Queen movements and figuring out where everything is safe
safePlacements :: [(Int, Int)] -> [(Int, Int)] -> [(Int, Int)]
safePlacements [] queen = []
safePlacements (x : chessBoard) queen
               | x `notElem` queen = x : safePlacements chessBoard queen
               | otherwise = safePlacements chessBoard queen

--Convert Tuples Cords to List Cords--
emptyListofLists :: Int -> [[Int]] ->[[Int]]
emptyListofLists chessBoard empty
               | chessBoard > 1 = []: emptyListofLists (chessBoard - 1) empty
               | otherwise = [[]]

conversion :: [[Int]] -> [(Int, Int)] -> [[Int]]
conversion board [] = board
conversion board (x:xs) = conversion (swapInList (fst x - 1) (snd x:(board !! (fst x-1))) board) xs

swapInList :: Int -> [Int] -> [[Int]] -> [[Int]]
swapInList x swappin list = first ++ (swappin:other)
                          where
                          (first, (_:other)) = splitAt x list


zeroesToEmpty :: [[Int]] -> [[Int]]
zeroesToEmpty [] = []
zeroesToEmpty (x:xs)
             | length x == 0 = [0]: zeroesToEmpty xs 
             | otherwise = (sort x): zeroesToEmpty xs

