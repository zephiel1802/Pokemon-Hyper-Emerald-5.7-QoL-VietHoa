local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local f = 0
local A_KEY = 1
local B_KEY = 2

callbacks:add('frame', function()
    f = f + 1
    
    -- Dismiss level up and exp share (0..400)
    if f < 400 then
        if (f % 15) < 5 then emu:setKeys(A_KEY) else emu:setKeys(0) end
        return
    end
    
    -- Walk in grass (400..850)
    if f >= 400 and f < 850 then
        local cycle = (f - 400) % 60
        if cycle < 30 then emu:setKeys(32) else emu:setKeys(16) end -- Right / Left
        return
    end
    
    -- From frame 850 onwards: press A every 25 frames
    if f >= 850 and f <= 1600 then
        if (f % 25) < 5 then
            emu:setKeys(A_KEY)
        else
            emu:setKeys(0)
        end
    end
    
    -- Capture frames during battle intro and mon send-out
    if f == 1000 then emu:screenshot(DIR .. 'fresh_battle_1000.png') end
    if f == 1100 then emu:screenshot(DIR .. 'fresh_battle_1100.png') end
    if f == 1150 then emu:screenshot(DIR .. 'fresh_battle_1150.png') end
    if f == 1200 then emu:screenshot(DIR .. 'fresh_battle_1200.png') end
    if f == 1250 then emu:screenshot(DIR .. 'fresh_battle_1250.png') end
    if f == 1300 then emu:screenshot(DIR .. 'fresh_battle_1300.png') end
    if f == 1350 then emu:screenshot(DIR .. 'fresh_battle_1350.png') end
    if f == 1400 then emu:screenshot(DIR .. 'fresh_battle_1400.png') end
    if f == 1500 then emu:screenshot(DIR .. 'fresh_battle_1500.png') end
    if f == 1600 then
        emu:screenshot(DIR .. 'fresh_battle_1600.png')
        local fh = io.open(DIR .. 'fresh_battle_done.txt', 'w')
        fh:write('done')
        fh:close()
    end
end)
