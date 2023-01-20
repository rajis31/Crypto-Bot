<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('ohlc', function (Blueprint $table) {
            $table->id();
            $table->timestamps();
            $table->string("symbol");
            $table->integer("time");
            $table->decimal("low",15,2);
            $table->decimal("high",15,2);
            $table->decimal("open",15,2);
            $table->decimal("close",15,2);
            $table->integer("volume");
        });
    }
    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('ohlc');
    }
};
