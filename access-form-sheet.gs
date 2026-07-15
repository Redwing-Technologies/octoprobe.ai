/**
 * OctoProbe AI — Access Request → Google Sheets
 *
 * SETUP (one-time):
 *  1. Open the Google Sheet you want submissions to land in.
 *  2. Click Extensions → Apps Script.
 *  3. Delete any placeholder code and paste this entire file.
 *  4. Save (Ctrl+S / Cmd+S).
 *  5. Click Deploy → New deployment.
 *       Type: Web app
 *       Execute as: Me
 *       Who has access: Anyone
 *  6. Click Deploy, authorise when prompted.
 *  7. Copy the Web App URL shown at the end.
 *  8. Paste that URL into the ENDPOINT constant in docs/index.html.
 *
 * To redeploy after edits: Deploy → Manage deployments → Edit (pencil) → New version → Deploy.
 */

// ── CONFIG ──────────────────────────────────────────────────────────────────

/** Tab name inside the spreadsheet. Created automatically if it doesn't exist. */
const SHEET_NAME = 'Access Requests';

/** Column order written to the sheet. Add/remove fields as needed. */
const COLUMNS = [
  'submitted_at',
  'name',
  'role',
  'organization',
  'email',
  'sector',
  'intended_use',
  'page_url',
];

/** Optional: send a notification email for each new submission. Set to '' to disable. */
const NOTIFY_EMAIL = 'team@octoprobe.ai';

// ── HANDLER ─────────────────────────────────────────────────────────────────

function doPost(e) {
  try {
    const payload = JSON.parse(e.postData.contents);
    writeRow(payload);
    if (NOTIFY_EMAIL) sendNotification(payload);
  } catch (err) {
    // Log silently — never surface errors to the public endpoint
    console.error('doPost error:', err);
  }

  // Apps Script Web Apps called with mode:'no-cors' can't return CORS headers,
  // but the write always succeeds. Return a plain JSON acknowledgement anyway.
  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok' }))
    .setMimeType(ContentService.MimeType.JSON);
}

// ── HELPERS ─────────────────────────────────────────────────────────────────

function getOrCreateSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    // Write header row
    sheet.appendRow(COLUMNS.map(c => c.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())));
    sheet.getRange(1, 1, 1, COLUMNS.length)
      .setFontWeight('bold')
      .setBackground('#0a0e15')
      .setFontColor('#38bdf8');
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function writeRow(data) {
  const sheet = getOrCreateSheet();
  const row = COLUMNS.map(col => data[col] || '');
  sheet.appendRow(row);
}

function sendNotification(data) {
  const subject = `OctoProbe Access Request — ${data.organization || data.email || 'Unknown'}`;
  const body = [
    `New access request received at ${data.submitted_at || new Date().toISOString()}`,
    '',
    `Name:         ${data.name || '—'}`,
    `Role:         ${data.role || '—'}`,
    `Organization: ${data.organization || '—'}`,
    `Email:        ${data.email || '—'}`,
    `Sector:       ${data.sector || '—'}`,
    `Use case:     ${data.intended_use || '—'}`,
    '',
    `Source URL:   ${data.page_url || '—'}`,
  ].join('\n');

  GmailApp.sendEmail(NOTIFY_EMAIL, subject, body);
}
