import { Controller } from '@hotwired/stimulus';

const STATE_PAUSED = 0;
const STATE_LOADING = 1;
const STATE_PLAYING = 2;

/**
 * Format the time from seconds to MM:SS.
 * @param {Number} time
 * @return {String}
 */
export function formatTime(time) {
  if (time === Infinity) {
    return '--:--';
  }

  const min = Math.floor(time / 60);
  const sec = Math.round(time - min * 60);

  return `${min.toString().padStart(2, 0)}:${sec.toString().padStart(2, 0)}`;
}

export default class extends Controller {
  /**
   * The map of HTMLMediaElement events and related class method listeners.
   * They will be automatically added to the Audio object once the controller
   * is connected and removed when it is disconnected.
   */
  static _audioEventsMap = new Map([
    ['error', '_onError'],
    ['ended', '_onEnd'],
    ['play', '_onPlay'],
    ['pause', '_onPause'],
    ['playing', '_onPlaying'],
    ['suspend', '_onSuspend'],
    ['waiting', '_onWaiting'],
    ['seeked', '_onSeeked'],
    ['seeking', '_onSeeking'],
    ['timeupdate', '_onTimeUpdate'],
    ['durationchange', '_onDurationChange'],
  ]);

  initialize() {
    // Initialize a new AudioPlayer instance and store it in Window to make it
    // persistent across navigation when using Turbo
    if (!window.currentAudio) {
      const audio = new Audio();
      audio.autoplay = false;
      audio.preload = 'metadata';

      window.currentAudio = audio;
    }

    this.audio = window.currentAudio;

    // Bind event handlers to use them in connect() and disconnect()
    for (const methodName of this.constructor._audioEventsMap.values()) {
      this[methodName] = this[methodName].bind(this);
    }
  }

  connect() {
    for (const [event, methodName] of this.constructor._audioEventsMap) {
      this.audio.addEventListener(event, this[methodName]);
    }
  }

  disconnect() {
    for (const [event, methodName] of this.constructor._audioEventsMap) {
      this.audio.removeEventListener(event, this[methodName]);
    }
  }

  // Getters

  /**
   * Whether a song is currently being played.
   * @return {Boolean}
   */
  get isPlaying() {
    return this.audio.paused === false;
  }

  /**
   * Whether a song is set and can be played.
   * @return {Boolean}
   */
  get canPlay() {
    return this.audio.currentSrc !== '' && this.audio.readyState > 0;
  }

  // Actions

  /**
   * Play the current song or resume playback.
   */
  play() {
    if (!this.canPlay) {
      throw new Error('No song has been loaded or is ready yet');
    }

    if (this.isPlaying) {
      throw new Error('The song is already playing');
    }

    this.audio.play();
  }

  /**
   * Pause the currently played song.
   */
  pause() {
    if (!this.canPlay) {
      throw new Error('No song has been loaded or is ready yet');
    }

    if (!this.isPlaying) {
      throw new Error('The song is already paused');
    }

    this.audio.pause();
  }

  /**
   * Toggle the playing state.
   */
  toggle() {
    if (this.isPlaying) {
      this.pause();
    } else {
      this.play();
    }
  }

  // CSS Classes

  static classes = ['loading', 'playing', 'visible'];

  // Targets

  static targets = [
    'currentTime',
    'duration',
    'progressSlider',
    'toggler',
    'playlistToggler',
  ];

  currentTimeTargetConnected(element) {
    this._updateCurrentTimeElement(element);
  }

  durationTargetConnected(element) {
    this._updateDurationElement(element);
  }

  progressSliderTargetConnected(element) {
    element._inputListener = ({ target }) => this._seek(target.value);
    element.addEventListener('input', element._inputListener);

    this._updateProgressSliderElement(element);
  }

  progressSliderTargetDisconnected(element) {
    element.removeEventListener('input', element._inputListener);
  }

  playlistTogglerTargetConnected(element) {
    element._clickListener = () => this._togglePlaylist();
    element.addEventListener('click', element._clickListener);
  }

  playlistTogglerTargetDisconnected(element) {
    element.removeEventListener('click', element._clickListener);
  }

  // Values

  static values = {
    autoplay: Boolean,
    url: String,
  };

  urlValueChanged() {
    if (this.audio.currentSrc !== this.urlValue) {
      if (this.isPlaying) {
        this.audio.pause();
      }

      if (this.urlValue) {
        this.audio.src = this.urlValue;

        // Force the loading state to don't wait for the audio events which
        // could be delayed depending on the browser or the network
        this._setState(STATE_LOADING);

        this.audio.load();
      } else {
        // We just reset the currentTime since setting an empty 'src' value
        // may have unexpected behavior when the urlValue will change again
        this.audio.currentTime = 0;
      }
    }

    if (this.autoplayValue && this.urlValue && !this.isPlaying) {
      this.audio.play();
    }
  }

  // Private methods

  /**
   * Set the current time of the loaded song.
   * @param {Number} percentage - The percentage to the song duration.
   */
  _seek(percentage) {
    if (!this.canPlay) {
      throw new Error('No song has been loaded or is ready yet');
    }

    if (percentage > 100) {
      percentage = 100;
    } else if (percentage < 0) {
      percentage = 0;
    }

    this.audio.currentTime = percentage
      ? this.audio.duration * (percentage / 100)
      : 0;
  }

  _setState(value) {
    if (value === STATE_LOADING) {
      this.togglerTarget.setAttribute('disabled', true);

      this.togglerTarget.classList.remove(...this.playingClasses);
      this.togglerTarget.classList.add(...this.loadingClasses);
    } else {
      this.togglerTarget.removeAttribute('disabled');

      if (value === STATE_PLAYING) {
        this.togglerTarget.classList.remove(...this.loadingClasses);
        this.togglerTarget.classList.add(...this.playingClasses);
      } else {
        this.togglerTarget.classList.remove(
          ...this.loadingClasses,
          ...this.playingClasses
        );
      }
    }
  }

  _updateCurrentTimeElement(element) {
    element.innerText = formatTime(this.audio.currentTime);
  }

  _updateDurationElement(element) {
    element.innerText = this.audio.duration
      ? formatTime(this.audio.duration)
      : '--:--';
  }

  _updateProgressSliderElement(element) {
    const { currentTime, duration } = this.audio;
    const progress = duration ? (currentTime / duration) * 100 : 0;

    element.value = progress;
    element.style.setProperty('--value', `${progress}%`);
    element.setAttribute('aria-valuenow', currentTime);

    if (duration) {
      element.removeAttribute('disabled');
    } else {
      element.setAttribute('disabled', true);
    }
  }

  _togglePlaylist() {
    const isVisible =
      this.playlistTogglerTarget.getAttribute('aria-expanded') === 'true';

    this.playlistTogglerTargets.forEach((element) => {
      element.setAttribute('aria-expanded', !isVisible);
    });
  }

  // Events handlers

  _onError() {
    this._setState(STATE_PAUSED);

    this.audio.currentTime = 0;
    this._onTimeUpdate();

    console.error(
      `Unable to load audio from ${this.urlValue} (${this.audio.error.message})`
    );
  }

  _onPlay() {
    this._setState(STATE_PLAYING);
  }

  _onPause() {
    this._setState(STATE_PAUSED);
  }

  _onEnd() {
    this._setState(STATE_PAUSED);

    if (window.Unicorn) {
      window.Unicorn.call('player', 'next');
    }
  }

  _onPlaying() {
    this._setState(this.isPlaying ? STATE_PLAYING : STATE_PAUSED);
  }

  _onSuspend() {
    this._setState(this.isPlaying ? STATE_PLAYING : STATE_PAUSED);
  }

  _onWaiting() {
    this._setState(STATE_LOADING);
  }

  _onSeeked() {
    if (this.audio.paused === true) {
      this._setState(STATE_PAUSED);
    }
  }

  _onSeeking() {
    // Consider seeking for the loading state too only when the sound is
    // paused since it will generally not be handled by 'waiting' event.
    if (this.audio.paused === true) {
      this._setState(STATE_LOADING);
    }
  }

  _onTimeUpdate() {
    this.currentTimeTargets.forEach((element) => {
      this._updateCurrentTimeElement(element);
    });

    this.progressSliderTargets.forEach((element) => {
      this._updateProgressSliderElement(element);
    });
  }

  _onDurationChange() {
    this.durationTargets.forEach((element) => {
      this._updateDurationElement(element);
    });

    this.progressSliderTargets.forEach((element) => {
      this._updateProgressSliderElement(element);
    });
  }
}
