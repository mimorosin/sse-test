/**
 * my-custom-lib/constants — Labrador user-defined component fixture
 * Fixture signature: LABRADOR_FIXTURE_MYCUSTOMLIB_CONSTANTS_V1
 */
'use strict';

const FIXTURE_TAG = 'labrador-user-defined-component-fixture';
const VERSION = '1.0.0';

const LIMITS = Object.freeze({
  MAX_RETRIES: 5,
  MAX_TIMEOUT_MS: 60000,
  MAX_PAYLOAD_BYTES: 1048576
});

const ERROR_CODES = Object.freeze({
  TIMEOUT: 'E_FIXTURE_TIMEOUT',
  INVALID: 'E_FIXTURE_INVALID',
  OVERFLOW: 'E_FIXTURE_OVERFLOW'
});

module.exports = {
  FIXTURE_TAG: FIXTURE_TAG,
  VERSION: VERSION,
  LIMITS: LIMITS,
  ERROR_CODES: ERROR_CODES
};
