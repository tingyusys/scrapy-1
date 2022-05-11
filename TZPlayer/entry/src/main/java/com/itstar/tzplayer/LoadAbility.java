package com.itstar.tzplayer;

import com.itstar.tzplayer.slice.LoadAbilitySlice;
import ohos.aafwk.ability.Ability;
import ohos.aafwk.content.Intent;

public class LoadAbility extends Ability {
    @Override
    public void onStart(Intent intent) {
        super.onStart(intent);
        super.setMainRoute(LoadAbilitySlice.class.getName());
    }
}
