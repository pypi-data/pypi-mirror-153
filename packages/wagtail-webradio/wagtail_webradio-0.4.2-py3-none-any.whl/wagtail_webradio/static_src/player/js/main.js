import { Application } from '@hotwired/stimulus';
import delegate from 'delegate-it';

import PlayerController from './controller';

const application = Application.start();
application.register('player', PlayerController);

/**
 * Data API implementation
 */

const ATTR_PLAYER_ADD = 'data-player-add';
const ATTR_PLAYER_ADD_PODCAST = 'data-player-add-podcast';
const ATTR_PLAYER_AUTOPLAY = 'data-player-autoplay';

// Listen to the click event on elements with an attribute 'data-player-add'
// which must define the song as a Python dict, and add it to the playlist. If
// there is an attribute 'data-player-autoplay', the song will be played once
// added.
//
// For example:
//
//     <button data-player-add="{'title': 'Title', 'url': '…'}">Add</button>
//
delegate(document, `[${ATTR_PLAYER_ADD}]`, 'click', (event) => {
  const component = window.Unicorn.getComponent('player');

  const target = event.delegateTarget;
  const song = target.getAttribute(ATTR_PLAYER_ADD);
  const autoplay = target.hasAttribute(ATTR_PLAYER_AUTOPLAY) ? 'True' : 'False';

  component.callMethod(`add(${song}, ${autoplay})`, 0, null, (err) => {
    console.error(err);
  });
});

// Listen to the click event on elements with an attribute 'data-player-add-podcast'
// which must define the id of a Podcast object, and add it to the playlist. If
// there is an attribute 'data-player-autoplay', the song will be played once
// added.
//
// For example:
//
//     <button data-player-add-podcast="10" data-player-autoplay>Add</button>
//
delegate(document, `[${ATTR_PLAYER_ADD_PODCAST}]`, 'click', (event) => {
  const component = window.Unicorn.getComponent('player');

  const target = event.delegateTarget;
  const id = Number.parseInt(target.getAttribute(ATTR_PLAYER_ADD_PODCAST), 10);
  const autoplay = target.hasAttribute(ATTR_PLAYER_AUTOPLAY) ? 'True' : 'False';

  component.callMethod(`add_podcast(${id}, ${autoplay})`, 0, null, (err) => {
    console.error(err);
  });
});
