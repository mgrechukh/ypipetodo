## Dedication

I have made for my wife this project as a part of the home digital infrastructure, essential to facilitate safe environment for our little daughter.

Love you both so much.

## Architecture

Primary design decision is to use free online Todo checklist in place of UI:

- ypipetodo runs as a background batch process ("headless worker");

- it receives links from [Todoist](https://todoist.com/);

- downloads with [yt-dlp](https://github.com/yt-dlp/yt-dlp);

- recode/remux to mp4 if needed;

- optionally asks [Emby media server](https://github.com/MediaBrowser/Emby) to rescan media directory.

End user receives download status as well as a progress feedback via task state and comments. No other interaction supposed neither required.

## How to use

0. You share youtube video from your phone as a Todo-item => soon have it appeared at Emby. That's it.

### Details

1. Tasks queue is a "Project" in term of Todoist. Ypipetodo needs only ProjectID and API Token. Single worker supports single project, no concurrency supported currently.

2. Each section within the Project represents subdirectory, e.g.: "Minecraft", "Halloween", "Carols", etc. Directory structure at Emby side created automatically. Default noname section is ignored (it can be used as scrapboard to prepare tasks before moving them to a work queue).

3. Only task "content" (title) and not "description" part is taken into account. Task may contain multiple links to process. 

4. Task is being marked as closed after successful download. It can later be reopened manually.

5. Unsuccessful download leaves task opened and puts comment explaining what happened. Put any other comment to force retry.

5. More documentation is probably needed with screenshots...

## Backend choice

Despite my own daily usage of [Todoist](https://todoist.com/), I attempted to make codebase modular and components clearly separated. It should be quiet easy to implement support for any other backend, kinda, RTM, Google Keep, or [Hass](https://www.home-assistant.io/), and a little bit more work needed to make backend configurable at runtime. I honestly would be glad to accept MRs. 

## Naming

"pipe" may refer here to both *tube and pipeline.
