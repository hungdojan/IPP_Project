<?php

require_once 'statsfile.php';
require_once 'error.php';

/**
 * Class Stats
 * @brief XXX Staticka trida ukladajici statistiky
 */
class Stats
{
    // public int $loc       = 0;
    // public int $comments  = 0;
    // public int $labels    = 0;
    // public int $jumps     = 0;
    // public int $fwjumps   = 0;
    // public int $backjumps = 0;
    // public int $badjumps  = 0;
    /** @var Table with all stats */
    public array $lof_stats = array( 
        "--loc"       => 0,
        "--comments"  => 0,
        "--labels"    => 0,
        "--jumps"     => 0,
        "--fwjumps"   => 0,
        "--backjumps" => 0,
        "--badjumps"  => 0
    );
    /** @var List of StatsFile instances */
    private array $lof_files;
    private array $used_file_names;

    /**
     * @breif Constructor of the class Stats
     */
    public function __construct()
    {
        // TODO:
    }

    /**
     * @brief Push new instance of StatsFile to $lof_files
     *
     * Check if file_path (output file destination) is unique.
     * If not the function returns given error code.
     *
     * @param $flags List of chosen flags
     * @param file_name Output fil destination
     * @return 0 or error code
     */
    public function appendStatsInstance(array $flags, string $file_path)
    {
        // checks whether file_path is already in use
        if (in_array($file_path, $used_file_names))
            return 99; // TODO: error code

        array_push($lof_files, new StatsFile($flags, $file_path));
        array_push($used_file_names, $file_path);
        return Error::NO_ERROR;
    }

    /**
     * @brief Creates all statistics file
     *
     * @return 0 or error code
     */
    public function flushFiles()
    {
        // Go through all instances of StatsFile
        // and creates a file for each of them
        foreach ($lof_sf as $item)
            $item->flushFile($lof_stats);
    }
}

$g_stats = null;

?>
