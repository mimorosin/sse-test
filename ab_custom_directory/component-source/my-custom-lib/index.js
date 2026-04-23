/**
 * my-custom-lib — Labrador user-defined component fixture
 * Fixture signature: LABRADOR_FIXTURE_MYCUSTOMLIB_ENTRY_V1
 */
'use strict';

const { clamp, formatDuration } = require('./utils');
const { FIXTURE_TAG, VERSION, LIMITS } = require('./constants');

function createSession(id, options) {
  const opts = options || {};
  return {
    id: String(id),
    tag: FIXTURE_TAG,
    version: VERSION,
    retries: clamp(opts.retries || 0, 0, LIMITS.MAX_RETRIES),
    timeoutMs: clamp(opts.timeoutMs || 1000, 100, LIMITS.MAX_TIMEOUT_MS),
    createdAt: 0
  };
}

function describeSession(session) {
  return session.id + '@' + session.version + ' (timeout=' + formatDuration(session.timeoutMs) + ')';
}

module.exports = {
  createSession: createSession,
  describeSession: describeSession,
  FIXTURE_TAG: FIXTURE_TAG,
  VERSION: VERSION
};
