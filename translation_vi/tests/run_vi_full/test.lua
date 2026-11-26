DIR='/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/run_vi_full/'
MAXF=18000

local NL = string.char(10)
local LOG = io.open(DIR .. "poc_log.txt", "w")
local function w(s) LOG:write(s .. NL); LOG:flush() end
local A, B, START, RIGHT, LEFT, UP, DOWN = 0, 1, 3, 4, 5, 6, 7
local CB2 = 0x030022C4
local STRVAR4 = 0x02021FC4          -- gStringVar4: the expanded text of the current message box

-- Gen3 charmap subset for the log
local CH = {[0x00]=" ", [0xAB]="!", [0xAC]="?", [0xAD]=".", [0xAE]="-", [0xB0]="…", [0xB1]="\"", [0xB2]="\"",
            [0xB4]="'", [0xB8]=",", [0xBA]="/", [0xF0]=":", [0x1B]="é", [0x5C]="(", [0x5D]=")"}
for i = 0, 9 do CH[0xA1 + i] = string.char(48 + i) end
for i = 0, 25 do CH[0xBB + i] = string.char(65 + i); CH[0xD5 + i] = string.char(97 + i) end
local function readtext(a)
  local out, n = {}, 0
  while n < 600 do
    local b = emu:read8(a + n)
    if b == 0xFF then break end
    if b == 0xFE then out[#out + 1] = "\\n" elseif b == 0xFA then out[#out + 1] = "\\l"
    elseif b == 0xFB then out[#out + 1] = "\\p"
    elseif b == 0xFC then out[#out + 1] = "{FC}"; n = n + 1
    elseif b == 0xFD then out[#out + 1] = "{BUF}"; n = n + 1
    else out[#out + 1] = CH[b] or string.format("{%02X}", b) end
    n = n + 1
  end
  return table.concat(out)
end

local f, last, shots, hangF, lasthash, lastF, pages = 0, "", 0, 0, 0, 0, 0
local NAMING = 0x080E4F59
local finished = false
local seenow = false

local function finish(msg)
  finished = true
  w(msg)
  local fh = io.open(DIR .. "poc_done.txt", "w"); fh:write(msg); fh:close()
end

callbacks:add("frame", function()
  if finished then return end
  f = f + 1
  emu:clearKeys(0x3FF)
  local c = f % 48
  local cb = emu:read32(CB2)
  if cb == 0x08085E5D then seenow = true end
  if cb == NAMING then                                   -- naming screen: START = cursor to OK, then A
    local d = f % 60
    if d < 3 then emu:addKey(START) elseif d >= 30 and d < 33 then emu:addKey(A) end
  elseif string.find(last, "Want to watch it", 1, true) and f - lastF < 300 then   -- skip memory cutscenes: No
    if c < 3 or (c >= 24 and c < 27) then emu:addKey(B) end
  elseif c < 3 then emu:addKey(A)
  elseif seenow and c >= 40 and c < 43 and f % 480 < 48 then emu:addKey(B)
  elseif seenow and c >= 12 and c < 30 then
    local phase = math.floor(f / 600) % 4
    emu:addKey(({RIGHT, DOWN, RIGHT, UP})[phase + 1])
  end
  if f % 8 == 0 then
    local t = readtext(STRVAR4)
    if t ~= last and #t > 2 then
      last = t; lastF = f; shots = shots + 1
      w(string.format("[%6d] %s", f, t))
      if shots <= 150 and not seenow then emu:screenshot(string.format("%spoc_%03d.png", DIR, shots)) end
    end
  end
  -- once in the field: capture every page as it is shown, right before A advances it
  if seenow and c == 47 and f - lastF < 1500 and pages < 300 then
    pages = pages + 1
    emu:screenshot(string.format("%spage_%03d_m%03d.png", DIR, pages, shots))
  end
  if f % 600 == 0 then
    w(string.format("-- frame %d cb2 %08X", f, emu:read32(CB2)))
    if f % 3000 == 0 then emu:screenshot(string.format("%stick_%06d.png", DIR, f)) end
  end
  if f >= MAXF then finish("done: " .. shots .. " messages, " .. f .. " frames") end
end)
