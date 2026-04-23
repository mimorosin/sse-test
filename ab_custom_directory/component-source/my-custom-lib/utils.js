/**
 * my-custom-lib/utils — Labrador user-defined component fixture
 * Fixture signature: LABRADOR_FIXTURE_MYCUSTOMLIB_UTILS_V1
 */
'use strict';

function clamp(value, min, max) {
  if (value < min) return min;
  if (value > max) return max;
  return value;
}

function formatDuration(ms) {
  if (ms < 1000) return ms + 'ms';
  const seconds = Math.floor(ms / 1000);
  const remainder = ms % 1000;
  if (remainder === 0) return seconds + 's';
  return seconds + 's ' + remainder + 'ms';
}

function toFixtureKey(namespace, name) {
  return 'LABRADOR_FIXTURE_' + String(namespace).toUpperCase() + '_' + String(name).toUpperCase();
}

module.exports = {
  clamp: clamp,
  formatDuration: formatDuration,
  toFixtureKey: toFixtureKey
};
