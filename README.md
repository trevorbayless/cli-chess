<p align="center">
  <a href="#"><img src="https://user-images.githubusercontent.com/3620552/214357735-53c2174c-5ada-45a2-97cb-6a25b5ca9c0c.png"/></a>
</p>

<p align="center">
A highly customizable way to play chess in your terminal. Supports online play (via Lichess.org) and
offline play against the Fairy-Stockfish engine. All Lichess variants are supported.
</p>

## Main Features
- Play online using your Lichess.org account
- Play offline against the Fairy-Stockfish engine
- Supports playing all Lichess [variants](https://lichess.org/variant)
- Theme the chess board and pieces to the colors of your choice
- Supports making moves in UCI, SAN, or LAN
- Play blindfold chess
- Watch Lichess TV

## Getting started
1. Open your terminal and run `pip install cli-chess`
2. Type `cli-chess` to start
3. Use your keyboard arrows, tab, or click to navigate the menus. Multi value menu options
   (e.g. changing the variant) can be cycled by pressing spacebar, enter, or by clicking
   on the value.

## Playing Online
In order to play online using your Lichess account you will need to create an API token for cli-chess to
authenticate with. Follow the steps below to create the token and register it with cli-chess. Generally, these
steps will only need to be run once as cli-chess will remember the API token.

1. Open your browser and login to your Lichess account
2. Click [here](https://lichess.org/account/oauth/token/create?scopes[]=board:play&scopes[]=challenge:read&scopes[]=challenge:write&description=cli-chess+token)
    to create a Lichess API token for cli-chess to authenticate with _(**NOTE**: Do not uncheck any of the
    token permissions as these are required by cli-chess)_
3. Click "Create"
4. Highlight and copy the token
5. Run cli-chess using the following command: `cli-chess --token ****` _(replace *'s with your API token)_

## Questions
#### 1. How do I make a move?
Moves are case-sensitive and must be made in SAN, LAN, or UCI. Moves cannot be made using the mouse.
Pawn promotions must specify the promotion piece type (e.g. `e8=Q` or `e7e8q`).
Moves that are ambiguous must specify the _from square_ when using SAN (e.g. `Ncd6`).
To drop a piece in Crazyhouse, use the `@` symbol (e.g. `Q@g4`). 

If you need more information on move notation, see Appendix C of [FIDE Laws of Chess](https://www.fide.com/FIDE/handbook/LawsOfChess.pdf).

#### 2. How do I increase the size of the board?
The only way to increase the size of the board is to increase the size of the
font you're using. Many terminals also support `Ctrl +` to increase the terminal size.

#### 3. The board or chess pieces aren't aligned or displaying properly, how can I fix this?
As cli-chess is a terminal based program, it has been designed to be used
with a monospace type font. A monospace font should always be used in order for
character alignment to be consistent. The display of cli-chess can change drastically
depending on the font being used, so it's important to choose a font that works best 
for your terminal and display preferences. The fonts that I have found to work best with
cli-chess for piece alignment are `Ubuntu Mono`, `MS Gothic`, and `NSimSun`.

#### 4. What operating systems are supported?
Development is mainly focused to support Linux. While cli-chess will work on
other operating systems (such as Windows and macOS) the support priority will
be directed towards Linux. Regardless of operating system please report any issues
found, and I will do my best to support.

#### 5. Can I use a different chess engine?
Playing offline vs the computer is _currently_ only directly compatible with the [Fairy-Stockfish](<https://fairy-stockfish.github.io/>) engine.
For simplicity, the Fairy-Stockfish binaries come pre-built with cli-chess for Linux, Windows, and macOS _(x86_64 architecture)_.

#### 6. What versions of Python are supported?
Python >= 3.7
