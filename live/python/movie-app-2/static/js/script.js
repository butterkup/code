$(async function () {
  /* Contants */
  const page_number_template = $("#template-page-number"),
    movie_box_template = $("#template-movie-box"),
    movie_row = $("#movie-row"),
    page_row = $("#page-row"),
    paginate = $("#paginate"),
    player = $("#main-player");

  const CONTENT_SIZE = 15,
    PAGE_NUMBER_SIZE = 5,
    NOSRC = "#!",
    RL_CNT = Math.floor((PAGE_NUMBER_SIZE - 1) / 2),
    MID = RL_CNT + 1,
    PREV_KEYS = ["p"],
    NEXT_KEYS = ["n"],
    MOVIE_SOURCE_URL = "/source/movies/$name",
    PREVIEW_SOURCE_URL = "/source/previews/$name",
    THUMBNAIL_SOURCE_URL = "/source/thumbnail/$name",
    VOLUME_CHANGE_STEP = 0.05,
    VIDEO_PLAYBACK_STEP = 5;

  let currentPreview = null,
    CURRENT_PAGE_NUMBER = 0,
    currentPlaying = null;
   const TOTAL_SIZE = await _loadMovies(0);

  adjustPageNumbers(CURRENT_PAGE_NUMBER);

  async function getMovies(offset, limit = CONTENT_SIZE) {
    return await $.ajax(`/api/movies?offset=${offset}&limit=${limit}`);
  }

  async function getMovie(movie_id) {
    return await $.ajax(`/api/movie/${movie_id}`);
  }

  function adjustPageNumbers(pageNumber) {
    const lastPage = Math.floor(TOTAL_SIZE / CONTENT_SIZE);
    let start = pageNumber - RL_CNT,
      end = pageNumber + RL_CNT;
    if (pageNumber < MID) {
      start = 0;
      end = PAGE_NUMBER_SIZE - 1;
    } else if (pageNumber >= lastPage - RL_CNT) {
      end = lastPage;
      start = lastPage - PAGE_NUMBER_SIZE + 1;
    }
    if (start < 0) start = 0;
    if (end > lastPage) end = lastPage;
    CURRENT_PAGE_NUMBER = pageNumber;
    if (pageNumber < 0) CURRENT_PAGE_NUMBER = 0;
    else if (pageNumber > lastPage) CURRENT_PAGE_NUMBER = lastPage;
    page_row.html("");
    let current;
    for (let i = start; i <= end; i++) {
      current = createPageNumber(i + 1);
      if (i == CURRENT_PAGE_NUMBER) current.addClass("bg-secondary");
      else current.addClass("bg-warning");
      page_row.append(current);
    }
    return CURRENT_PAGE_NUMBER;
  }

  function createMovieBox(index, { thumbnail, movie_id, movie, preview }) {
    let elem = document.createElement("div");
    elem.innerHTML = movie_box_template
      .html()
      .replaceAll("$index", index)
      .replaceAll("$movie", movie)
      .replaceAll("$preview", preview)
      .replaceAll("$thumbnail", thumbnail)
      .replaceAll("$id-movie", movie_id);
    elem = $(elem.children[0]);
    if (movie_id == player.attr("data-movie-id")) elem.addClass("current");
    return elem;
  }

  function createPageNumber(pageNumber) {
    const elem = document.createElement("div");
    elem.innerHTML = page_number_template
      .html()
      .replaceAll("$number", pageNumber);
    return $(elem.children[0]);
  }

  async function _loadMovies(pageNumber) {
    const { movies, total } = await getMovies(pageNumber * CONTENT_SIZE);
    movie_row.html("");
    movies.forEach((movie, index) => {
      movie_row.append(createMovieBox(index, movie));
    });
    $(document.body).scrollTop(0);
    return total;
  }

  async function loadMovies(pageNumber) {
    if (pageNumber == CURRENT_PAGE_NUMBER) return;
    adjustPageNumbers(pageNumber);
    return await _loadMovies(CURRENT_PAGE_NUMBER);
  }

  function subNameURL(mobj) {
    mobj.movie = MOVIE_SOURCE_URL.replace("$name", mobj.movie);
    mobj.thumbnail = THUMBNAIL_SOURCE_URL.replace("$name", mobj.thumbnail);
    mobj.preview = PREVIEW_SOURCE_URL.replace("$name", mobj.preview);
    return mobj;
  }

  function setPlayer({ movie, preview, movie_id, thumbnail }) {
    player.attr("src", movie);
    player.attr("data-movie-id", movie_id);
    player.attr("data-thumbnail", thumbnail);
    player.attr("data-preview", preview);
    player.focus();
  }

  function setNewCurrentPlaying(video) {
    setPlayer({
      movie: video.attr("data-movie"),
      thumbnail: video.attr("data-thumbnail"),
      preview: video.attr("data-preview"),
      movie_id: video.attr("data-movie-id"),
    });
    if (currentPlaying) currentPlaying.parent().removeClass("current");
    currentPlaying = video;
  }
  async function setNextMovie() {
    const nextToPlay = Number.parseInt(player.attr("data-movie-id")) + 1;
    if (nextToPlay >= TOTAL_SIZE) nextToPlay = 0;
    const movie = await getMovie(nextToPlay);
    setPlayer(subNameURL(movie));
  }
  async function setPrevMovie() {
    const nextToPlay = Number.parseInt(player.attr("data-movie-id")) - 1;
    if (nextToPlay < 0) nextToPlay = TOTAL_SIZE - 1;
    const movie = await getMovie(nextToPlay);
    setPlayer(subNameURL(movie));
  }

  const clicked = (keys, key) => keys.includes(key.toLowerCase());

  $(document.body).on("keyup", (event) => {
    const boxes = $(".movie-box");
    if (clicked(["m"], event.key)) player[0].muted = !player[0].muted;
    else if (boxes.length > 0 && !currentPlaying) setNewCurrentPlaying($(boxes[0]).children());
    else if (clicked(PREV_KEYS, event.key)) setPrevMovie();
    else if (clicked(NEXT_KEYS, event.key)) setNextMovie();
  });
  player.on("ended", setNextMovie);
  player.on("keydown", (event) => {
    if (clicked(["arrowup"], event.key)) {
      if (player[0].volume >= 1 - VOLUME_CHANGE_STEP) player[0].volume = 1;
      else player[0].volume += VOLUME_CHANGE_STEP;
    } else if (clicked(["arrowdown"], event.key)) {
      if (player[0].volume <= VOLUME_CHANGE_STEP) player[0].volume = 0;
      else player[0].volume -= VOLUME_CHANGE_STEP;
    } else if (clicked(["arrowright"], event.key)) {
      if (player[0].currentTime >= player[0].duration - VIDEO_PLAYBACK_STEP) player[0].currentTime = player[0].duration - 2;
      else player[0].currentTime += VIDEO_PLAYBACK_STEP;
    } else if (clicked(["arrowleft"], event.key)) {
      if (player[0].currentTime <= VIDEO_PLAYBACK_STEP) player[0].currentTime = 0;
      else player[0].currentTime -= VIDEO_PLAYBACK_STEP;
    }
  });
  movie_row.delegate(".movie-box", "mouseenter", function () {
    const video = $(this).children();
    video.attr("src", video.attr("data-preview"));
  });
  movie_row.delegate(".movie-box", "mouseleave", function () {
    $(this).children().attr("src", NOSRC);
  });
  movie_row.delegate(".movie-box", "click", function () {
    setNewCurrentPlaying($(this).children());
  });
  movie_row.delegate(".movie-box", "touchmove", function () {
    const video = $(this).children();
    if (currentPreview) {
      if (currentPreview.attr("src") === video.attr("src")) return;
      else currentPreview.attr("src", NOSRC);
    }
    currentPreview = video;
    video.attr("src", video.attr("data-preview"));
  });
  paginate.delegate(".page-number", "click", async function () {
    await loadMovies(Number.parseInt($(this).text()) - 1);
  });
  $("#page-next").on("click", async function () {
    await loadMovies(CURRENT_PAGE_NUMBER + PAGE_NUMBER_SIZE);
  });
  $("#page-prev").on("click", async function () {
    await loadMovies(CURRENT_PAGE_NUMBER - PAGE_NUMBER_SIZE);
  });
  $("#page-next").on("dblclick", async function () {
    await loadMovies(CURRENT_PAGE_NUMBER + PAGE_NUMBER_SIZE * 2);
  });
  $("#page-prev").on("dblclick", async function () {
    await loadMovies(CURRENT_PAGE_NUMBER - PAGE_NUMBER_SIZE * 2);
  });
});
