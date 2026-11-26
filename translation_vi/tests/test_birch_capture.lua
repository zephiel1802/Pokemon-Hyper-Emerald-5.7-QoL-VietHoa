DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/run_vi_full/'

local NL = string.char(10)
local A, B, START, RIGHT, LEFT, UP, DOWN = 0, 1, 3, 4, 5, 6, 7
local CB2 = 0x030022C4
local STRVAR4 = 0x02021FC4

local f = 0
local birched = false
local finished = false

callbacks:add("frame", function()
  if finished then return end
  f = f + 1
  emu:clearKeys(0x3FF)
  
  -- Frame 0 .. 900: Title screen -> press A / START to enter New Game
  if f < 900 then
    if f % 30 < 3 then emu:addKey(A) end
    if f % 60 < 3 then emu:addKey(START) end
  end
  
  -- Around frame 1050 .. 1250: Birch appears and speaks his very first line!
  if f >= 1050 and f <= 1300 and not birched then
    if f == 1150 or f == 1200 or f == 1250 then
      emu:screenshot(string.format("%sbirch_intro_vi_%04d.png", DIR, f))
      birched = true
    end
  end
  
  if f >= 1350 then
    finished = true
  end
end)
