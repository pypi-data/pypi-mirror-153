#!/usr/bin/env perl

# For the most part, this was adapted from
# https://github.com/aces/surface-extraction/blob/7c9c5987a2f8f5fdeb8d3fd15f2f9b636401d9a1/scripts/marching_cubes.pl.in
#
# o 2022-05-06
#   Replaced `inflate_to_sphere` with `inflate_to_sphere_implicit`


use strict;
use warnings "all";
use File::Temp qw/ tempdir /;
use Getopt::Tabular;

use MNI::Startup;
use MNI::FileUtilities;

my $license = <<LICENSE;
Copyright Alan C. Evans
Professor of Neurology
McGill University
LICENSE

my $usage = <<USAGE;
Usage: $ProgramName [-left|-right] [-inflate 2000 2000] surface_unknown.obj surface_81920.obj

$license
USAGE


my $side = undef;
my @inflate_args = undef;
my @options = (
  ['-left', 'const', "Left", \$side, "Surface is a left surface"],
  ['-right', 'const', "Right", \$side, "Surface is a right surface (sphere should be flipped)"],
  ['-inflate', 'integer', 2, \@inflate_args, "Use inflate_to_sphere_implicit instead of inflate_to_sphere, and pass the given arguments to it."]
);

GetOptions( \@options, \@ARGV ) or exit 1;
die "$usage\n" unless @ARGV == 2;
my $input_file = shift;
my $output_file = shift;



my $tmpdir = &tempdir( "interpolate-sphere-XXXXXX", TMPDIR => 1, CLEANUP => 1 );

# Coarsen and smooth the original marching-cubes surface.

#my $white_surface_sm = "${tmpdir}/white_surf_sm.obj";
#&run( 'adapt_object_mesh', $white_surface, $white_surface_sm, 120000, 1, 50, 1 );

# skip smoothing
my $white_surface_sm = $input_file;

# Inflate the white surface onto a unit sphere.

my $white_sphere_sm = "${tmpdir}/white_sphere_sm.obj";

if ( @inflate_args ) {
  &run( 'inflate_to_sphere_implicit', $white_surface_sm, $white_sphere_sm, $inflate_args[0], $inflate_args[1] );
}
else {
  &run( 'inflate_to_sphere', $white_surface_sm, $white_sphere_sm );
}

# Interpolate from sphere-to-sphere to resample the white surface
# using the 40962 vertices on the standard ICBM surface average
# template. This unit sphere is the one used for surface registration.

my $unit_sphere = "${tmpdir}/unit_sphere.obj";
&run( 'create_tetra', $unit_sphere, 0, 0, 0, 1, 1, 1, 81920 );
if( $side eq "Right" ) {
  &run( "param2xfm", "-scales", -1, 1, 1,
        "${tmpdir}/flip.xfm" );
  &run( "transform_objects", $unit_sphere,
        "${tmpdir}/flip.xfm", $unit_sphere );
  unlink( "${tmpdir}/flip.xfm" );
}

# Evaluate the white surface from the marching-cubes surface.

&resample_white_surface( $white_surface_sm, $white_sphere_sm,
                         $unit_sphere, $output_file );


# Resample the white surface from a standard sphere from the
# hi-res marching-cubes white surface. The distribution of
# vertices on the sphere is adapted such as to produce an
# interpolated surface with triangles of nearly the same size.

sub resample_white_surface {

  my $white_mc = shift;     # hi-res raw marching-cubes surface
  my $sphere_mc = shift;    # sphere corresponding to white_mc
  my $unit_sphere = shift;  # standard sphere
  my $output = shift;       # output white surface with uniform triangles

  my @conf = ( { 'size' => 320,     # most of the motion occurs early
                 'fwhm' => 20.0,
                 'niter' => 500 },
               { 'size' => 1280,
                 'fwhm' => 10.0,
                 'niter' => 500 },
               { 'size' => 5120,
                 'fwhm' => 5.0,
                 'niter' => 300 },
               { 'size' => 20480,
                 'fwhm' => 2.0,
                 'niter' => 150 } );

  my $start = 320;
  my $end = 20480;

  my $npolys = `print_n_polygons $unit_sphere`;
  chomp( $npolys );

  my $current_sphere = "${tmpdir}/current_sphere.obj";
  &run( 'cp', '-f', $unit_sphere, $current_sphere );

  # obtain initial white surface

  &run( 'interpolate_sphere', $white_mc, $sphere_mc,
        $current_sphere, $output );

  # Multi-resolution approach from coarse to fine mesh.

  for( my $idx = 0; $idx <= $#conf; $idx++ ) {

    my $size = $conf[$idx]{size};

    next if( $size < $start );
    last if( $size > $end );

    print "Sphere adaptation at $size vertices...\n";

    # Obtain the triangle areas from current white surface to
    # the current sphere at size npolys.

    my $white_area = "${tmpdir}/white_area.txt";
    my $sphere_area = "${tmpdir}/sphere_area.txt";
    &run( 'depth_potential', '-area_simple', $output, $white_area );
    &run( 'depth_potential', '-area_simple', $current_sphere, $sphere_area );
    &run( 'vertstats_math', '-old_style_file', '-div', $white_area,
          $sphere_area, $white_area );
    unlink( $sphere_area );
    if( $conf[$idx]{fwhm} > 0 ) {
      &run( 'depth_potential', '-smooth', $conf[$idx]{fwhm},
            $white_area, $output, $white_area );
    }

    # adapt the current_sphere at this size based on the areas.

    &subdivide_mesh( $current_sphere, $size, $current_sphere );
    &run( 'adapt_metric', $current_sphere, $white_area,
          $current_sphere, $conf[$idx]{niter} );
    unlink( $white_area );

    # interpolate relative to the original white surface at npolys.

    &subdivide_mesh( $current_sphere, $npolys, $current_sphere );
    &run( 'interpolate_sphere', $white_mc, $sphere_mc,
          $current_sphere, $output );

  }

  unlink( $current_sphere );

}


# Check if the input surface has the same side orientation (left)
# as the default template model.

sub CheckFlipOrientation {

  my $obj = shift;

  my $npoly = `print_n_polygons $obj`;
  chomp( $npoly );

  my $ret = `tail -5 $obj`;
  my @verts = split( ' ', $ret );
  my @last3 = ( $verts[$#verts-2], $verts[$#verts-1], $verts[$#verts] );

  my $dummy_sphere = "${tmpdir}/dummy_sphere.obj";
  &run('create_tetra',$dummy_sphere,0,0,0,1,1,1,$npoly);
  $ret = `tail -5 $dummy_sphere`;
  unlink( $dummy_sphere );
  @verts = split( ' ', $ret );
  my @sphere3 = ( $verts[$#verts-2], $verts[$#verts-1], $verts[$#verts] );
  if( $last3[0] == $verts[$#verts-2] &&
      $last3[1] == $verts[$#verts-1] &&
      $last3[2] == $verts[$#verts-0] ) {
    return 0;
  } else {
    return 1;
  }
}


# subdivide a surface taking into account if it's a left or right hemisphere.

sub subdivide_mesh {

  my $input = shift;
  my $npoly = shift;
  my $output = shift;

  my $npoly_input = `print_n_polygons $input`;
  chomp( $npoly_input );
  if( !CheckFlipOrientation( $input ) ) {
    &run( "subdivide_polygons", $input, $output, $npoly );
  } else {
    # flip right as left first before subdividing, then flip back.
    &run( "param2xfm", '-clobber', '-scales', -1, 1, 1,
          "${tmpdir}/flip.xfm" );
    my $input_flipped = "${tmpdir}/right_flipped.obj";
    &run( "transform_objects", $input,
          "${tmpdir}/flip.xfm", $input_flipped );
    &run( "subdivide_polygons", $input_flipped, $output, $npoly );
    &run( "transform_objects", $output,
          "${tmpdir}/flip.xfm", $output );  # flip.xfm is its own inverse
    unlink( $input_flipped );
    unlink( "${tmpdir}/flip.xfm" );
  }
}


# Execute a system call.

sub run {
  print "@_\n";
  system(@_)==0 or die "Command @_ failed with status: $?";
}
